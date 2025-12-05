"""
Complete Flow Test Script

Tests the entire payroll + settlement flow without starting a server.
"""

import sys
from decimal import Decimal
from backend.models import PayrollRequest, EmployeePayrollInput
from backend.bridge import process_payroll
from backend.coinbase_client import CoinbaseClient

def test_payroll_processing():
    """Test COBOL payroll processing"""
    print("=" * 60)
    print("🧟‍♂️ TEST 1: COBOL PAYROLL PROCESSING")
    print("=" * 60)
    print()
    
    # Create test payroll request
    request = PayrollRequest(
        employees=[
            EmployeePayrollInput(
                employee_id="EMP001",
                hours_worked=Decimal("40.00"),
                hourly_rate=Decimal("25.50"),
                tax_code="US",
                wallet_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2"
            ),
            EmployeePayrollInput(
                employee_id="EMP002",
                hours_worked=Decimal("35.00"),
                hourly_rate=Decimal("30.00"),
                tax_code="US",
                wallet_address="0x1234567890123456789012345678901234567890"
            ),
            EmployeePayrollInput(
                employee_id="EMP003",
                hours_worked=Decimal("45.00"),
                hourly_rate=Decimal("22.00"),
                tax_code="US",
                wallet_address="0xabcdefabcdefabcdefabcdefabcdefabcdefabcd"
            )
        ]
    )
    
    print(f"Processing payroll for {len(request.employees)} employees...")
    print()
    
    try:
        response = process_payroll(request)
        
        print("✅ Payroll Processing Complete!")
        print()
        print(f"Summary: {response.summary['processed']} processed, {response.summary['errors']} errors")
        print()
        
        for result in response.results:
            print(f"Employee: {result.employee_id}")
            print(f"  Gross Pay: ${result.gross_pay}")
            print(f"  Federal Tax: ${result.federal_tax}")
            print(f"  State Tax: ${result.state_tax}")
            print(f"  Net Pay: ${result.net_pay}")
            print(f"  Status: {result.status}")
            print(f"  Wallet: {result.wallet_address}")
            print()
        
        return response
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def test_settlement(payroll_response):
    """Test mock settlement"""
    print("=" * 60)
    print("🧟‍♂️ TEST 2: MOCK SETTLEMENT")
    print("=" * 60)
    print()
    
    if not payroll_response:
        print("❌ Skipping settlement test - no payroll response")
        return
    
    print("Initializing CoinbaseClient (MOCK)...")
    client = CoinbaseClient(network="base-sepolia")
    print()
    
    print("Executing batch settlement...")
    print()
    
    try:
        settlement_result = client.batch_settle(payroll_response)
        
        print("✅ Settlement Complete!")
        print()
        print(f"Total Processed: {settlement_result['total_processed']}")
        print(f"Total Succeeded: {settlement_result['total_succeeded']}")
        print(f"Total Failed: {settlement_result['total_failed']}")
        print()
        
        for result in settlement_result['results']:
            status_icon = "✅" if result['status'] == 'success' else "❌"
            print(f"{status_icon} {result.get('employee_id', 'N/A')}: {result['amount']} USDC")
            if result['status'] == 'success':
                print(f"   TX: {result['transaction_hash'][:20]}...")
            else:
                print(f"   Error: {result.get('error', 'Unknown')}")
            print()
        
        return settlement_result
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        return None


def test_error_handling():
    """Test error handling"""
    print("=" * 60)
    print("🧟‍♂️ TEST 3: ERROR HANDLING")
    print("=" * 60)
    print()
    
    client = CoinbaseClient(network="base-sepolia")
    
    # Test 1: Invalid address
    print("Test 3.1: Invalid wallet address")
    try:
        result = client.transfer_usdc(
            to_address="invalid_address",
            amount=Decimal("10.00"),
            employee_id="TEST"
        )
        print(f"❌ Should have raised InvalidAddressError")
    except Exception as e:
        print(f"✅ Caught expected error: {type(e).__name__}")
    print()
    
    # Test 2: Insufficient balance
    print("Test 3.2: Insufficient balance")
    client.mock_balance = Decimal("1.00")
    try:
        result = client.transfer_usdc(
            to_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2",
            amount=Decimal("1000.00"),
            employee_id="TEST"
        )
        print(f"❌ Should have raised InsufficientFundsError")
    except Exception as e:
        print(f"✅ Caught expected error: {type(e).__name__}")
    print()
    
    # Test 3: Negative amount
    print("Test 3.3: Negative amount")
    try:
        result = client.transfer_usdc(
            to_address="0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2",
            amount=Decimal("-10.00"),
            employee_id="TEST"
        )
        print(f"❌ Should have raised ValueError")
    except Exception as e:
        print(f"✅ Caught expected error: {type(e).__name__}")
    print()


def main():
    """Run all tests"""
    print()
    print("🧟‍♂️" * 30)
    print("LEDGER-DE-MAIN: COMPLETE FLOW TEST")
    print("🧟‍♂️" * 30)
    print()
    
    # Test 1: Payroll Processing
    payroll_response = test_payroll_processing()
    
    # Test 2: Settlement
    if payroll_response:
        settlement_result = test_settlement(payroll_response)
    
    # Test 3: Error Handling
    test_error_handling()
    
    print("=" * 60)
    print("🎉 ALL TESTS COMPLETE!")
    print("=" * 60)
    print()


if __name__ == "__main__":
    main()
