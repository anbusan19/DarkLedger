"""
Manual Settlement Transfer Test Script

This script tests a single USDC transfer to a known test address.
It loads the wallet from environment variables and executes a test transfer.

Usage:
    export PAYROLL_WALLET_ID=your-wallet-id
    python backend/test_settlement.py

Or provide a custom test address and amount:
    python backend/test_settlement.py 0xYourTestAddress 1.50

Requirements:
- PAYROLL_WALLET_ID or PAYROLL_WALLET_SEED must be set
- COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY must be set
- Wallet must have sufficient USDC balance
"""

import sys
from decimal import Decimal

from backend.coinbase_client import CoinbaseClient


# Default test address (Base Sepolia testnet)
# This is a known test address - replace with your own for testing
DEFAULT_TEST_ADDRESS = "0x742d35Cc6634C0532925a3b844Bc9e7595f0bEb2"
DEFAULT_TEST_AMOUNT = Decimal("0.10")  # 10 cents USDC


def main():
    """
    Execute a test USDC transfer and display transaction details.
    
    This is THE BODY executing a test blockchain transfer with THE BRAIN's precision.
    """
    print("=" * 60)
    print("🧟‍♂️ FRANKENSTEIN SETTLEMENT TEST")
    print("=" * 60)
    print()
    
    # Parse command line arguments
    test_address = DEFAULT_TEST_ADDRESS
    test_amount = DEFAULT_TEST_AMOUNT
    
    if len(sys.argv) > 1:
        test_address = sys.argv[1]
        print(f"📍 Using custom address: {test_address}")
    else:
        print(f"📍 Using default test address: {test_address}")
    
    if len(sys.argv) > 2:
        test_amount = Decimal(sys.argv[2])
        print(f"💵 Using custom amount: {test_amount} USDC")
    else:
        print(f"💵 Using default amount: {test_amount} USDC")
    
    print()
    
    # Initialize CoinbaseClient with base-sepolia
    print("🔧 Initializing CoinbaseClient (base-sepolia)...")
    client = CoinbaseClient(network="base-sepolia")
    print()
    
    # Load wallet from environment variable (handled by _ensure_wallet)
    print("🔑 Loading wallet from environment...")
    wallet_address = client._ensure_wallet()
    print(f"✅ Wallet Loaded: {wallet_address}")
    print()
    
    # Check current balance
    print("💰 Checking wallet balance...")
    balance = client.get_balance(asset="usdc")
    print(f"   Current Balance: {balance} USDC")
    
    if balance < test_amount:
        print()
        print("❌ ERROR: Insufficient balance for test transfer")
        print(f"   Required: {test_amount} USDC")
        print(f"   Available: {balance} USDC")
        print()
        print("💡 TIP: Run setup_testnet_wallet.py to request faucet funds")
        sys.exit(1)
    
    print()
    
    # Execute test transfer to known test address
    print("🚀 Executing test transfer...")
    print(f"   To: {test_address}")
    print(f"   Amount: {test_amount} USDC")
    print()
    
    result = client.transfer_usdc(
        to_address=test_address,
        amount=test_amount,
        employee_id="TEST_EMPLOYEE"
    )
    
    print()
    print("=" * 60)
    print("📊 TRANSACTION RESULT")
    print("=" * 60)
    print()
    
    # Print transaction hash and link
    if result["status"] == "success":
        print(f"✅ Status: {result['status'].upper()}")
        print(f"🔗 Transaction Hash: {result['transaction_hash']}")
        print(f"🌐 Transaction Link: {result['transaction_link']}")
        print(f"⏰ Timestamp: {result['timestamp']}")
        print(f"💵 Amount: {result['amount']} USDC")
        print(f"📍 To Address: {result['to_address']}")
        print()
        print("=" * 60)
        print("🎉 TEST SUCCESSFUL!")
        print("=" * 60)
        print()
        print("Verify transaction on Basescan:")
        print(f"   {result['transaction_link']}")
        print()
    else:
        print(f"❌ Status: {result['status'].upper()}")
        print(f"⚠️  Error: {result.get('error', 'Unknown error')}")
        print(f"⏰ Timestamp: {result['timestamp']}")
        print(f"💵 Amount: {result['amount']} USDC")
        print(f"📍 To Address: {result['to_address']}")
        print()
        print("=" * 60)
        print("❌ TEST FAILED")
        print("=" * 60)
        sys.exit(1)


if __name__ == "__main__":
    main()
