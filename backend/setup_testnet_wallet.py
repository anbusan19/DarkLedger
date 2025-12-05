"""
Testnet Wallet Setup Script

This script initializes a new wallet on Base Sepolia testnet,
requests faucet funds, and displays the wallet information.

Usage:
    python backend/setup_testnet_wallet.py

The script will:
1. Create a new wallet on base-sepolia
2. Request USDC from the testnet faucet
3. Display wallet ID and balance
4. Provide instructions for persisting the wallet ID
"""

from backend.coinbase_client import CoinbaseClient


def main():
    """
    Set up a new testnet wallet with faucet funds.
    
    This is THE BODY preparing for blockchain operations with testnet funds.
    """
    print("=" * 60)
    print("🧟‍♂️ FRANKENSTEIN TESTNET WALLET SETUP")
    print("=" * 60)
    print()
    
    # Initialize CoinbaseClient with base-sepolia
    print("🔧 Initializing CoinbaseClient (base-sepolia)...")
    client = CoinbaseClient(network="base-sepolia")
    print()
    
    # Create new wallet and print wallet address
    print("🔨 Creating new wallet...")
    wallet_address = client.create_wallet()
    print(f"✅ Wallet Created!")
    print(f"   Wallet Address: {wallet_address}")
    print()
    
    # Request faucet funds
    print("🚰 Requesting testnet USDC from faucet...")
    print("   (This may take 10-30 seconds...)")
    client.request_faucet(asset="usdc")
    print("✅ Faucet request completed!")
    print()
    
    # Check and print balance
    print("💰 Checking wallet balance...")
    balance = client.get_balance(asset="usdc")
    print(f"✅ Balance: {balance} USDC")
    print()
    
    # Print persistence instructions
    print("=" * 60)
    print("📝 NEXT STEPS:")
    print("=" * 60)
    print()
    print("To use this wallet in your application, set the environment variable:")
    print()
    print(f"   export PAYROLL_WALLET_ADDRESS={wallet_address}")
    print()
    print("Or add it to your .env file:")
    print()
    print(f"   PAYROLL_WALLET_ADDRESS={wallet_address}")
    print()
    print("=" * 60)
    print("🎉 Setup Complete! Your MOCK wallet is ready for testing.")
    print("=" * 60)


if __name__ == "__main__":
    main()
