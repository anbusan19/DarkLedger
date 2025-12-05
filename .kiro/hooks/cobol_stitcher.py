import os
from cdp import Cdp, Wallet

def pay_employee(address: str, amount_usdc: float):
    """
    Pays an employee in USDC on Base.
    """
    # 1. Configure SDK (Load keys from env)
    api_key_name = os.getenv("COINBASE_API_KEY_NAME")
    private_key = os.getenv("COINBASE_PRIVATE_KEY")
    Cdp.configure(api_key_name, private_key)

    # 2. Re-instantiate the payroll wallet (In prod, persist this wallet ID)
    # For Hackathon demo, creating a new one or loading from seed is fine.
    # wallet = Wallet.fetch(wallet_id) 
    print("🧟‍♂️ WALLET: Loading Payroll Wallet...")
    wallet = Wallet.create() # Creates a fresh wallet for demo purposes
    
    # 3. Request Faucet Funds (Only for Testnet Demo!)
    # print("💧 FAUCET: Draining testnet USDC...")
    # wallet.faucet("usdc").wait()

    # 4. Execute Transfer
    print(f"💸 PAYING: Sending {amount_usdc} USDC to {address}...")
    transfer = wallet.transfer(amount_usdc, "usdc", address).wait()
    
    return transfer.transaction_link