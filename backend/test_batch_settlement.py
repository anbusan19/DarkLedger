"""
Batch Settlement Test Script

This script tests batch settlement with multiple employees.
It creates a mock PayrollResponse with 3 employees and executes
batch settlement, displaying the summary and transaction details.

Usage:
    export PAYROLL_WALLET_ID=your-wallet-id
    python backend/test_batch_settlement.py

Requirements:
- PAYROLL_WALLET_ID or PAYROLL_WALLET_SEED must be set
- COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY must be set
- Wallet must have sufficient USDC balance for all transfers
"""

from decimal import Decimal

from backend.coinbase_client import CoinbaseClient
from backend.models import PayrollResponse, EmployeePayrollOutput


# Test wallet addresses for Base Sepolia testnet
# These are example addresses - replace with your own test addresses
TEST_ADDRESSES = [
    "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2",
    "0x1234567890123456789012345678901234567890",
    "0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
]


def create_mock_payroll_response() -> PayrollResponse:
    """
    Create a mock PayrollResponse with 3 employees for testing.
    
    This simulates the output from THE BRAIN (COBOL) with precise calculations.
    
    Returns:
        PayrollResponse: Mock payroll data with 3 employees
    """
    # Create mock PayrollResponse with 3 employees
    mock_results = [
        EmployeePayrollOutput(
            employee_id="EMP001",
            gross_pay=Decimal("1020.00"),
            federal_tax=Decimal("153.00"),
            state_tax=Decimal("51.00"),
            net_pay=Decimal("816.00"),
            status="OK",
            wallet_address=TEST_ADDRESSES[0]
        ),
        EmployeePayrollOutput(
            employee_id="EMP002",
            gross_pay=Decimal("1065.00"),
            federal_tax=Decimal("159.75"),
            state_tax=Decimal("53.25"),
            net_pay=Decimal("852.00"),
            status="OK",
            wallet_address=TEST_ADDRESSES[1]
        ),
        EmployeePayrollOutput(
            employee_id="EMP003",
            gross_pay=Decimal("900.00"),
            federal_tax=Decimal("135.00"),
            state_tax=Decimal("45.00"),
            net_pay=Decimal("720.00"),
            status="OK",
            wallet_address=TEST_ADDRESSES[2]
        )
    ]
    
    return PayrollResponse(
        results=mock_results,
        summary={
            "processed": 3,
            "errors": 0
        }
    )


def main():
    """
    Execute batch settlement test and display results.
    
    This is THE BODY executing batch blockchain transfers with THE BRAIN's precision.
    """
    print("=" * 60)
    print("🧟‍♂️ FRANKENSTEIN BATCH SETTLEMENT TEST")
    print("=" * 60)
    print()
    
    # Initialize CoinbaseClient with base-sepolia
    print("🔧 Initializing CoinbaseClient (base-sepolia)...")
    client = CoinbaseClient(network="base-sepolia")
    print()
    
    # Load wallet from environment
    print("🔑 Loading wallet from environment...")
    wallet = client._ensure_wallet()
    print(f"✅ Wallet Loaded: {wallet.id}")
    print()
    
    # Check current balance
    print("💰 Checking wallet balance...")
    balance = client.get_balance(asset="usdc")
    print(f"   Current Balance: {balance} USDC")
    print()
    
    # Create mock PayrollResponse with 3 employees
    print("📋 Creating mock PayrollResponse with 3 employees...")
    payroll_response = create_mock_payroll_response()
    
    # Calculate total amount needed
    total_needed = sum(
        result.net_pay 
        for result in payroll_response.results 
        if result.status == "OK"
    )
    
    print(f"   Employee 1: {payroll_response.results[0].employee_id} - {payroll_response.results[0].net_pay} USDC")
    print(f"   Employee 2: {payroll_response.results[1].employee_id} - {payroll_response.results[1].net_pay} USDC")
    print(f"   Employee 3: {payroll_response.results[2].employee_id} - {payroll_response.results[2].net_pay} USDC")
    print(f"   Total Required: {total_needed} USDC")
    print()
    
    if balance < total_needed:
        print("❌ ERROR: Insufficient balance for batch settlement")
        print(f"   Required: {total_needed} USDC")
        print(f"   Available: {balance} USDC")
        print()
        print("💡 TIP: Run setup_testnet_wallet.py to request faucet funds")
        return
    
    # Call batch_settle() and print summary
    print("🚀 Executing batch settlement...")
    print("   (This may take 30-60 seconds for 3 transactions...)")
    print()
    
    summary = client.batch_settle(payroll_response)
    
    print()
    print("=" * 60)
    print("📊 BATCH SETTLEMENT SUMMARY")
    print("=" * 60)
    print()
    print(f"✅ Total Processed: {summary['total_processed']}")
    print(f"✅ Total Succeeded: {summary['total_succeeded']}")
    print(f"❌ Total Failed: {summary['total_failed']}")
    print()
    
    # Print individual transaction details
    print("=" * 60)
    print("📝 INDIVIDUAL TRANSACTION DETAILS")
    print("=" * 60)
    print()
    
    for i, result in enumerate(summary['results'], 1):
        print(f"Transaction {i}:")
        print(f"   Employee ID: {result['employee_id']}")
        print(f"   Amount: {result['amount']} USDC")
        print(f"   Status: {result['status'].upper()}")
        
        if result['status'] == 'success':
            print(f"   Transaction Hash: {result['transaction_hash']}")
            print(f"   Transaction Link: {result['transaction_link']}")
            print(f"   Timestamp: {result['timestamp']}")
        else:
            print(f"   Error: {result.get('error', 'Unknown error')}")
        
        print()
    
    # Verify all transactions on Basescan
    print("=" * 60)
    print("🔍 VERIFY TRANSACTIONS ON BASESCAN")
    print("=" * 60)
    print()
    
    for i, result in enumerate(summary['results'], 1):
        if result['status'] == 'success':
            print(f"Transaction {i} ({result['employee_id']}):")
            print(f"   {result['transaction_link']}")
            print()
    
    # Final status
    if summary['total_failed'] == 0:
        print("=" * 60)
        print("🎉 BATCH SETTLEMENT TEST SUCCESSFUL!")
        print("=" * 60)
        print()
        print(f"All {summary['total_succeeded']} transactions completed successfully.")
        print("Verify the transactions on Basescan using the links above.")
    else:
        print("=" * 60)
        print("⚠️  BATCH SETTLEMENT COMPLETED WITH ERRORS")
        print("=" * 60)
        print()
        print(f"{summary['total_succeeded']} succeeded, {summary['total_failed']} failed")
        print("Review the error details above.")


if __name__ == "__main__":
    main()
