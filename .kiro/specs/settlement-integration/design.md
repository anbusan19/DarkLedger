# Design Document: Settlement Integration

## Overview

The Settlement Integration component bridges the gap between traditional payroll calculations and blockchain-based payments. It uses the Coinbase Developer Platform (CDP) SDK to execute USDC transfers on Base L2, providing instant, low-cost settlement with full transaction transparency.

The design emphasizes security (credential management, address validation), reliability (error handling, transaction confirmation), and flexibility (testnet/mainnet switching, batch processing).

## Architecture

### Component Diagram

```
Python Bridge (FastAPI)
    ↓
Settlement Integration (coinbase_client.py)
    ↓
Coinbase CDP SDK
    ↓
Base L2 Network (Sepolia/Mainnet)
```

### Settlement Flow

1. Python Bridge completes payroll processing
2. PayrollResponse contains net_pay for each employee
3. Settlement Integration receives PayrollResponse
4. For each employee with status="OK", validate wallet address
5. Execute USDC transfer via CDP SDK
6. Wait for transaction confirmation
7. Return settlement summary with transaction details

## Components and Interfaces

### CoinbaseClient Class

**Key Methods:**

```python
class CoinbaseClient:
    def __init__(self, network: str = "base-sepolia")
    def create_wallet() -> Wallet
    def load_wallet(wallet_id: str) -> Wallet
    def get_balance(asset: str = "usdc") -> Decimal
    def request_faucet(asset: str = "usdc") -> None
    def transfer_usdc(to_address: str, amount: Decimal, employee_id: str) -> dict
    def batch_settle(payroll_response: PayrollResponse) -> dict
```

**Transfer Result Format:**

```python
{
    "transaction_hash": str,
    "transaction_link": str,
    "status": "success" | "failed",
    "timestamp": str,
    "amount": Decimal,
    "to_address": str,
    "employee_id": str
}
```

**Batch Settlement Result:**

```python
{
    "total_processed": int,
    "total_succeeded": int,
    "total_failed": int,
    "results": [SettlementResult, ...]
}
```

## Transaction Execution Logic

### Transfer Flow

1. Validate wallet address format (0x + 40 hex chars)
2. Validate amount is positive
3. Check wallet balance is sufficient
4. Execute wallet.transfer(amount, "usdc", destination)
5. Wait for confirmation with .wait()
6. Extract transaction hash and link
7. Log result and return transaction details

### Error Handling

- InsufficientFundsError: Balance too low
- InvalidAddressError: Malformed wallet address
- TransactionFailedError: Blockchain transaction failed
- All errors logged with context (employee_id, amount, address)

### Batch Processing

- Filter only successful payroll results (status="OK")
- Execute transfers sequentially with error isolation
- Continue processing if one transfer fails
- Return summary with all results

## Wallet Management

### Wallet Persistence

```python
# Option 1: Wallet ID
PAYROLL_WALLET_ID = os.getenv("PAYROLL_WALLET_ID")
wallet = client.load_wallet(PAYROLL_WALLET_ID)

# Option 2: Seed phrase
PAYROLL_WALLET_SEED = os.getenv("PAYROLL_WALLET_SEED")
wallet = client.load_wallet_from_seed(PAYROLL_WALLET_SEED)
```

### Network Configuration

```python
COINBASE_NETWORK = os.getenv("COINBASE_NETWORK", "base-sepolia")
# Supported: "base-sepolia", "base-mainnet"
```

## Security Considerations

### Credential Security
- Load from environment variables only
- Never log API keys or private keys
- Validate on startup (fail fast)

### Transfer Limits
```python
MAX_TRANSFER_AMOUNT = Decimal("10000.00")  # $10,000 USDC per transaction
```

### Address Validation
```python
def _is_valid_address(address: str) -> bool:
    pattern = r'^0x[a-fA-F0-9]{40}$'
    return bool(re.match(pattern, address))
```

## Testing Strategy

### Unit Tests
1. Configuration with valid/invalid credentials
2. Wallet creation and loading
3. Address validation (valid/invalid formats)
4. Amount validation (positive/negative/zero)
5. Mocked transfer execution

### Integration Tests
6. Testnet wallet creation
7. Faucet fund requests
8. Real testnet transfers
9. Batch settlement with multiple employees

### Manual Testing
10. End-to-end payroll → settlement flow
11. Verify transactions on Basescan explorer

## Performance Considerations

- Base L2 block time: ~2 seconds
- Transaction confirmation: ~5-10 seconds
- Batch of 100 employees: ~10-15 minutes (sequential)

### Future Optimizations
- Async/parallel transfers using asyncio
- Smart contract multi-send for batch payments
- Rate limiting to avoid API throttling

## Deployment

### Environment Variables

```bash
# Required
export COINBASE_API_KEY_NAME="your-api-key-name"
export COINBASE_PRIVATE_KEY="your-private-key"

# Wallet (choose one)
export PAYROLL_WALLET_ID="wallet-id"
# OR
export PAYROLL_WALLET_SEED="seed phrase"

# Network
export COINBASE_NETWORK="base-sepolia"  # or "base-mainnet"
```

### Dependencies

```
cdp-sdk>=0.0.5
```

### Testnet Setup

```bash
# Create wallet and request faucet funds
python -c "from backend.coinbase_client import CoinbaseClient; \
           client = CoinbaseClient(); \
           wallet = client.create_wallet(); \
           client.request_faucet(); \
           print(f'Wallet: {wallet.id}, Balance: {client.get_balance()}')"
```

## Integration with Python Bridge

### Extended Data Models

```python
class EmployeePayrollInput(BaseModel):
    employee_id: str
    hours_worked: Decimal
    hourly_rate: Decimal
    tax_code: str
    wallet_address: str  # Add for settlement

class EmployeePayrollOutput(BaseModel):
    # ... existing fields ...
    wallet_address: str  # Add for settlement
```

### Combined Endpoint

```python
@app.post("/api/payroll/process-and-settle")
async def process_and_settle(request: PayrollRequest):
    # Process payroll
    payroll_response = process_payroll(request)
    
    # Execute settlement
    client = CoinbaseClient()
    settlement_summary = client.batch_settle(payroll_response)
    
    return {
        "payroll": payroll_response,
        "settlement": settlement_summary
    }
```

## Monitoring and Logging

### Transaction Logging

```python
logger.info(f"💸 Transfer: {employee_id}, {amount} USDC → {address}")
logger.info(f"✅ Confirmed: {tx_hash} ({duration}s)")
logger.error(f"❌ Failed: {employee_id}, {error}")
```

### Audit Trail

```python
# Write to data/settlement_audit.jsonl
{
    "timestamp": "2025-12-05T10:30:00Z",
    "employee_id": "EMP001",
    "amount": "816.00",
    "to_address": "0x742d35...",
    "transaction_hash": "0xabc123...",
    "status": "success",
    "network": "base-sepolia"
}
```

## Future Enhancements

1. Multi-asset support (ETH, DAI, etc.)
2. Scheduled recurring payroll
3. Payment splitting across multiple addresses
4. Automatic retry logic for failed transactions
5. Async/parallel processing for large batches
