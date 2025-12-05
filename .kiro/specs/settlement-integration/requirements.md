# Requirements Document

## Introduction

The Settlement Integration component handles cryptocurrency payments to employees using the Coinbase Developer Platform (CDP) SDK on Base Layer 2. It receives verified payroll calculations from the COBOL engine (via the Python Bridge), initializes secure wallet connections, and executes USDC transfers with transaction tracking. This component ensures that the audit-proof calculations from COBOL are settled instantly and cost-effectively on the blockchain, completing the "Frankenstein" architecture's promise of legacy precision with modern speed.

## Glossary

- **Settlement Integration**: The Python module that executes blockchain payments using the CDP SDK
- **CDP SDK**: Coinbase Developer Platform Software Development Kit for blockchain operations
- **Base L2**: Ethereum Layer 2 network optimized for low-cost, fast transactions
- **USDC**: USD Coin, a stablecoin pegged 1:1 to the US Dollar
- **Wallet**: Blockchain account that holds and transfers cryptocurrency
- **Transaction Hash**: Unique identifier for a blockchain transaction
- **Transaction Link**: URL to view transaction details on a block explorer
- **Gasless Transfer**: Transaction where gas fees are abstracted or sponsored
- **Base Sepolia**: Test network for Base L2 (for development and testing)
- **Base Mainnet**: Production network for Base L2 (for real transactions)
- **Faucet**: Service that provides free testnet tokens for development

## Requirements

### Requirement 1

**User Story:** As a System Administrator, I want the CDP SDK configured with secure credentials, so that the system can authenticate with Coinbase services.

#### Acceptance Criteria

1. THE Settlement Integration SHALL load API credentials using the key_manager module
2. THE Settlement Integration SHALL call Cdp.configure() with api_key_name and private_key
3. WHEN credentials are invalid, THE Settlement Integration SHALL raise an authentication error
4. THE Settlement Integration SHALL configure the SDK once at module initialization
5. THE Settlement Integration SHALL never log or expose credentials in error messages

### Requirement 2

**User Story:** As a Developer, I want wallet management abstracted into a reusable client, so that wallet operations are consistent and maintainable.

#### Acceptance Criteria

1. THE Settlement Integration SHALL provide a CoinbaseClient class for wallet operations
2. THE Settlement Integration SHALL support creating new wallets for testing
3. THE Settlement Integration SHALL support loading existing wallets by wallet_id
4. THE Settlement Integration SHALL support loading wallets from seed phrases
5. THE Settlement Integration SHALL persist wallet identifiers for reuse across sessions

### Requirement 3

**User Story:** As an Operator, I want to execute USDC transfers to employee wallet addresses, so that employees receive their net pay on the blockchain.

#### Acceptance Criteria

1. THE Settlement Integration SHALL accept employee wallet address as a string parameter
2. THE Settlement Integration SHALL accept net pay amount as a Decimal parameter
3. THE Settlement Integration SHALL execute transfers using wallet.transfer() method with amount, asset="usdc", and destination address
4. THE Settlement Integration SHALL wait for transaction confirmation using .wait() method
5. THE Settlement Integration SHALL return the transaction hash and transaction link

### Requirement 4

**User Story:** As a Developer, I want to use Base Sepolia for testing, so that I can develop without spending real money.

#### Acceptance Criteria

1. THE Settlement Integration SHALL default to Base Sepolia network for development
2. THE Settlement Integration SHALL support requesting testnet USDC from faucet
3. THE Settlement Integration SHALL provide a method to check wallet balance on testnet
4. THE Settlement Integration SHALL allow network configuration via environment variable
5. THE Settlement Integration SHALL clearly log which network is being used

### Requirement 5

**User Story:** As an Operator, I want transaction details returned after settlement, so that I can track and verify payments.

#### Acceptance Criteria

1. THE Settlement Integration SHALL return transaction hash as a string
2. THE Settlement Integration SHALL return transaction link (block explorer URL)
3. THE Settlement Integration SHALL return transaction status (success/failed)
4. THE Settlement Integration SHALL include timestamp of transaction execution
5. THE Settlement Integration SHALL log transaction details for audit purposes

### Requirement 6

**User Story:** As a System Integrator, I want settlement integrated with the payroll processing flow, so that payments are executed automatically after calculations.

#### Acceptance Criteria

1. THE Settlement Integration SHALL accept PayrollResponse from the Python Bridge
2. THE Settlement Integration SHALL iterate through all successful payroll results (status="OK")
3. THE Settlement Integration SHALL skip employees with error status (status="ER")
4. THE Settlement Integration SHALL execute one transfer per employee with net_pay amount
5. THE Settlement Integration SHALL return a list of settlement results with transaction details

### Requirement 7

**User Story:** As a Developer, I want comprehensive error handling for blockchain operations, so that failures are reported clearly and the system remains stable.

#### Acceptance Criteria

1. WHEN a wallet address is invalid, THE Settlement Integration SHALL raise a validation error
2. WHEN wallet balance is insufficient, THE Settlement Integration SHALL raise an insufficient funds error
3. WHEN a transfer fails, THE Settlement Integration SHALL capture the error and continue processing remaining employees
4. WHEN network connectivity fails, THE Settlement Integration SHALL raise a network error with retry guidance
5. THE Settlement Integration SHALL log all errors with context (employee_id, amount, address)

### Requirement 8

**User Story:** As a Security Engineer, I want wallet private keys secured, so that funds cannot be stolen or misused.

#### Acceptance Criteria

1. THE Settlement Integration SHALL never log wallet private keys or seed phrases
2. THE Settlement Integration SHALL store wallet seeds encrypted or in secure environment variables
3. THE Settlement Integration SHALL use the key_manager for all credential access
4. THE Settlement Integration SHALL validate wallet addresses before executing transfers
5. THE Settlement Integration SHALL implement transfer amount limits for safety (configurable maximum)

### Requirement 9

**User Story:** As an Operator, I want to switch between testnet and mainnet, so that I can test safely before deploying to production.

#### Acceptance Criteria

1. THE Settlement Integration SHALL read network configuration from COINBASE_NETWORK environment variable
2. THE Settlement Integration SHALL default to "base-sepolia" if not specified
3. THE Settlement Integration SHALL support "base-sepolia" and "base-mainnet" values
4. WHEN using mainnet, THE Settlement Integration SHALL log a warning about real funds
5. THE Settlement Integration SHALL prevent faucet requests on mainnet

### Requirement 10

**User Story:** As a Developer, I want batch settlement support, so that multiple employees can be paid efficiently in a single operation.

#### Acceptance Criteria

1. THE Settlement Integration SHALL provide a batch_settle() function that accepts multiple payment records
2. THE Settlement Integration SHALL execute transfers sequentially with error isolation
3. THE Settlement Integration SHALL collect all transaction results (success and failure)
4. THE Settlement Integration SHALL return a summary with total_processed, total_succeeded, total_failed counts
5. THE Settlement Integration SHALL continue processing remaining employees if one transfer fails
