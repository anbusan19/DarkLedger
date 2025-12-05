"""
Coinbase Client for Settlement Integration

Handles cryptocurrency payments using the Coinbase Developer Platform (CDP) SDK.
This is THE BODY executing blockchain transfers with THE BRAIN's precision.
"""

import logging
import os
import re
from decimal import Decimal
from typing import Optional

from cdp import Cdp, Wallet

from backend import key_manager
from backend.models import PayrollResponse


# Custom Exception Classes
class SettlementError(Exception):
    """Base exception for settlement operations"""
    pass


class InsufficientFundsError(SettlementError):
    """Raised when wallet balance is insufficient for transfer"""
    pass


class InvalidAddressError(SettlementError):
    """Raised when wallet address format is invalid"""
    pass


class TransactionFailedError(SettlementError):
    """Raised when blockchain transaction fails"""
    pass


# Configure logging
logger = logging.getLogger("settlement")
logger.setLevel(logging.INFO)
if not logger.handlers:
    handler = logging.StreamHandler()
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)


class CoinbaseClient:
    """
    Client for managing Coinbase CDP wallet operations and USDC transfers.
    
    Handles wallet initialization, balance checking, and settlement execution
    on Base L2 network (Sepolia testnet or Mainnet).
    """
    
    def __init__(self, network: str = "base-sepolia"):
        """
        Initialize CoinbaseClient with specified network.
        
        Args:
            network: Network to use ("base-sepolia" or "base-mainnet")
                    Defaults to "base-sepolia" for safe testing.
        """
        self.network = network
        self.wallet: Optional[Wallet] = None
        
        # Configure SDK on initialization
        self._configure_sdk()
    
    def _configure_sdk(self):
        """
        Configure the CDP SDK with API credentials from key_manager.
        
        This method:
        - Loads credentials securely from environment variables
        - Configures the CDP SDK for blockchain operations
        - Logs the network being used (with warning for mainnet)
        
        Raises:
            ValueError: If credentials are missing or invalid
        """
        try:
            # Get credentials from key_manager (Real work is done by key_manager)
            api_key_name, private_key = key_manager.key_manager.get_credentials()
            
            # Configure CDP SDK
            Cdp.configure(api_key_name, private_key)
            
            # Log network configuration
            if self.network == "base-mainnet":
                logger.warning(
                    f"⚠️  MAINNET MODE: Using {self.network} - REAL FUNDS AT RISK"
                )
            else:
                logger.info(f"🔧 SDK Configured: Network={self.network}")
                
        except ValueError as e:
            logger.error(f"❌ SDK Configuration Failed: {e}")
            raise
    
    def create_wallet(self) -> Wallet:
        """
        Create a new wallet for settlement operations.
        
        This method creates a new CDP wallet and stores it for future use.
        The wallet ID should be persisted (e.g., in environment variables)
        for reuse across sessions.
        
        Returns:
            Wallet: The newly created wallet instance
        """
        logger.info("🔨 Creating new wallet...")
        self.wallet = Wallet.create(network_id=self.network)
        logger.info(f"✅ Wallet Created: ID={self.wallet.id}")
        logger.info(f"💾 Persist this wallet ID: export PAYROLL_WALLET_ID={self.wallet.id}")
        return self.wallet
    
    def load_wallet(self, wallet_id: str) -> Wallet:
        """
        Load an existing wallet by its ID.
        
        Args:
            wallet_id: The unique identifier of the wallet to load
            
        Returns:
            Wallet: The loaded wallet instance
        """
        logger.info(f"📂 Loading wallet: {wallet_id}")
        self.wallet = Wallet.fetch(wallet_id)
        logger.info(f"✅ Wallet Loaded: ID={self.wallet.id}")
        return self.wallet
    
    def load_wallet_from_seed(self, seed: str) -> Wallet:
        """
        Load a wallet from its seed phrase.
        
        Args:
            seed: The seed phrase for the wallet
            
        Returns:
            Wallet: The imported wallet instance
        """
        logger.info("🌱 Importing wallet from seed...")
        self.wallet = Wallet.import_data(seed=seed, network_id=self.network)
        logger.info(f"✅ Wallet Imported: ID={self.wallet.id}")
        return self.wallet
    
    def _ensure_wallet(self) -> Wallet:
        """
        Ensure a wallet is initialized, loading or creating as needed.
        
        This method checks if a wallet is already loaded. If not, it attempts to:
        1. Load from PAYROLL_WALLET_ID environment variable
        2. Load from PAYROLL_WALLET_SEED environment variable
        3. Create a new wallet if neither is set
        
        Returns:
            Wallet: The initialized wallet instance
        """
        if self.wallet is not None:
            return self.wallet
        
        # Try loading from wallet ID
        wallet_id = os.getenv("PAYROLL_WALLET_ID")
        if wallet_id:
            logger.info("🔑 Initializing wallet from PAYROLL_WALLET_ID")
            return self.load_wallet(wallet_id)
        
        # Try loading from seed
        wallet_seed = os.getenv("PAYROLL_WALLET_SEED")
        if wallet_seed:
            logger.info("🔑 Initializing wallet from PAYROLL_WALLET_SEED")
            return self.load_wallet_from_seed(wallet_seed)
        
        # Create new wallet if neither is set
        logger.warning("⚠️  No wallet credentials found - creating new wallet")
        return self.create_wallet()
    
    def get_balance(self, asset: str = "usdc") -> Decimal:
        """
        Get the wallet balance for a specified asset.
        
        Args:
            asset: The asset to check balance for (default: "usdc")
            
        Returns:
            Decimal: The balance amount with full precision
        """
        # Ensure wallet is initialized
        self._ensure_wallet()
        
        # Get balance from wallet (Real work is done by CDP SDK)
        balance = self.wallet.balance(asset)
        
        logger.info(f"💰 Balance: {balance} {asset.upper()}")
        return Decimal(str(balance))
    
    def request_faucet(self, asset: str = "usdc") -> None:
        """
        Request testnet funds from the faucet.
        
        This method is only available on testnet (base-sepolia).
        It will raise an error if called on mainnet.
        
        Args:
            asset: The asset to request from faucet (default: "usdc")
            
        Raises:
            ValueError: If called on mainnet network
        """
        # Prevent faucet requests on mainnet
        if self.network == "base-mainnet":
            error_msg = "❌ Faucet not available on mainnet - use real funds"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Ensure wallet is initialized
        self._ensure_wallet()
        
        # Request faucet funds and wait for completion
        logger.info(f"🚰 Requesting faucet funds: {asset.upper()}...")
        faucet_tx = self.wallet.faucet(asset)
        faucet_tx.wait()
        
        logger.info(f"✅ Faucet request completed for {asset.upper()}")
    
    def _is_valid_address(self, address: str) -> bool:
        """
        Validate Ethereum wallet address format.
        
        Checks that the address:
        - Is not empty
        - Starts with '0x'
        - Contains exactly 40 hexadecimal characters after '0x'
        
        Args:
            address: The wallet address to validate
            
        Returns:
            bool: True if address is valid, False otherwise
        """
        # Check address is not empty
        if not address:
            return False
        
        # Validate format: 0x followed by 40 hex characters
        pattern = r'^0x[a-fA-F0-9]{40}$'
        return bool(re.match(pattern, address))
    
    def transfer_usdc(
        self, 
        to_address: str, 
        amount: Decimal, 
        employee_id: str = None
    ) -> dict:
        """
        Execute a USDC transfer to an employee wallet address.
        
        This method handles the complete transfer flow:
        1. Validates the destination address
        2. Validates the transfer amount
        3. Checks wallet balance is sufficient
        4. Executes the blockchain transfer
        5. Waits for transaction confirmation
        6. Returns transaction details
        
        Args:
            to_address: Destination wallet address (must be valid Ethereum address)
            amount: Amount of USDC to transfer (must be positive)
            employee_id: Optional employee identifier for logging and tracking
            
        Returns:
            dict: Transaction result containing:
                - transaction_hash: Blockchain transaction hash
                - transaction_link: URL to view transaction on block explorer
                - status: "success" or "failed"
                - timestamp: ISO format timestamp
                - amount: Transfer amount
                - to_address: Destination address
                - employee_id: Employee identifier (if provided)
                - error: Error message (only if status="failed")
                
        Raises:
            InvalidAddressError: If to_address format is invalid
            ValueError: If amount is not positive
            InsufficientFundsError: If wallet balance is too low
        """
        import time
        from datetime import datetime
        
        # Ensure wallet is initialized (Real work is done by CDP SDK)
        self._ensure_wallet()
        
        # Validate address format
        if not self._is_valid_address(to_address):
            error_msg = f"Invalid wallet address format: {to_address}"
            logger.error(f"❌ {error_msg}")
            raise InvalidAddressError(error_msg)
        
        # Validate amount is positive
        if amount <= 0:
            error_msg = f"Transfer amount must be positive, got: {amount}"
            logger.error(f"❌ {error_msg}")
            raise ValueError(error_msg)
        
        # Check balance is sufficient
        current_balance = self.get_balance("usdc")
        if current_balance < amount:
            error_msg = (
                f"Insufficient funds: Balance={current_balance} USDC, "
                f"Required={amount} USDC"
            )
            logger.error(f"❌ {error_msg}")
            raise InsufficientFundsError(error_msg)
        
        # Log transfer initiation
        employee_context = f" (Employee: {employee_id})" if employee_id else ""
        logger.info(
            f"💸 Transfer Initiated{employee_context}: "
            f"{amount} USDC → {to_address}"
        )
        
        # Execute transfer and handle confirmation
        try:
            start_time = time.time()
            
            # Execute the transfer (Real work is done by CDP SDK)
            transfer = self.wallet.transfer(
                amount=float(amount),
                asset_id="usdc",
                destination=to_address
            )
            
            # Wait for transaction confirmation
            transfer.wait()
            
            # Calculate execution duration
            duration = time.time() - start_time
            
            # Extract transaction details
            transaction_hash = transfer.transaction_hash
            transaction_link = transfer.transaction_link
            
            # Log successful transfer
            logger.info(
                f"✅ Transfer Confirmed{employee_context}: "
                f"{transaction_hash} ({duration:.2f}s)"
            )
            
            # Return success result
            return {
                "transaction_hash": transaction_hash,
                "transaction_link": transaction_link,
                "status": "success",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "amount": str(amount),
                "to_address": to_address,
                "employee_id": employee_id
            }
            
        except Exception as e:
            # Log error with context
            error_msg = str(e)
            logger.error(
                f"❌ Transfer Failed{employee_context}: {error_msg}"
            )
            
            # Return failure result
            return {
                "transaction_hash": None,
                "transaction_link": None,
                "status": "failed",
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "amount": str(amount),
                "to_address": to_address,
                "employee_id": employee_id,
                "error": error_msg
            }

    def batch_settle(self, payroll_response: PayrollResponse) -> dict:
        """
        Execute batch settlement for multiple employees from payroll results.
        
        This method processes all successful payroll results (status="OK") and
        executes USDC transfers to each employee's wallet address. It provides
        error isolation - if one transfer fails, processing continues for
        remaining employees.
        
        Args:
            payroll_response: PayrollResponse object containing processed payroll results
            
        Returns:
            dict: Batch settlement summary containing:
                - total_processed: Number of employees processed
                - total_succeeded: Number of successful transfers
                - total_failed: Number of failed transfers
                - results: List of individual settlement results
        """
        # Initialize results list and counters (Subtask 7.1)
        results = []
        succeeded = 0
        failed = 0
        
        # Filter payroll_response.results for status="OK" only (Subtask 7.1)
        valid_results = [
            result for result in payroll_response.results 
            if result.status == "OK"
        ]
        
        # Log batch settlement start with count of valid results (Subtask 7.1)
        logger.info(
            f"🚀 Batch Settlement Started: {len(valid_results)} employees to process"
        )
        
        # Iterate through filtered valid results (Subtask 7.2)
        for result in valid_results:
            # For each result, call transfer_usdc (Subtask 7.2)
            settlement_result = self.transfer_usdc(
                to_address=result.wallet_address,
                amount=result.net_pay,
                employee_id=result.employee_id
            )
            
            # Append settlement result to results list (Subtask 7.2)
            results.append(settlement_result)
            
            # Increment succeeded or failed counter based on status (Subtask 7.2)
            if settlement_result["status"] == "success":
                succeeded += 1
            else:
                failed += 1
            
            # Continue processing even if one transfer fails (error isolation) (Subtask 7.2)
            # This is handled by the try-except in transfer_usdc which returns
            # a result dict with status="failed" instead of raising an exception
        
        # Build summary dict (Subtask 7.3)
        summary = {
            "total_processed": len(valid_results),
            "total_succeeded": succeeded,
            "total_failed": failed,
            "results": results
        }
        
        # Log batch settlement completion with success/failure counts (Subtask 7.3)
        logger.info(
            f"✅ Batch Settlement Complete: "
            f"{succeeded} succeeded, {failed} failed out of {len(valid_results)} total"
        )
        
        # Return summary dict (Subtask 7.3)
        return summary
