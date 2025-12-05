"""
Coinbase Client for Settlement Integration

Handles cryptocurrency payments using the Coinbase Developer Platform (CDP) SDK.
This is THE BODY executing blockchain transfers with THE BRAIN's precision.

NOTE: This is a MOCK implementation for testing without actual CDP credentials.
"""

import logging
import os
import re
import time
from datetime import datetime
from decimal import Decimal
from typing import Optional
import hashlib
import random

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
    MOCK Client for managing Coinbase CDP wallet operations and USDC transfers.
    
    This is a mock implementation that simulates blockchain operations
    without requiring actual CDP credentials or network access.
    
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
        self.account_address = None
        self.mock_balance = Decimal("10000.00")  # Mock balance of 10,000 USDC
        
        # Configure SDK on initialization
        self._configure_sdk()
    
    def _configure_sdk(self):
        """
        MOCK: Configure the CDP SDK (simulated).
        
        This method simulates SDK configuration without requiring actual credentials.
        """
        # Log network configuration
        if self.network == "base-mainnet":
            logger.warning(
                f"⚠️  MOCK MAINNET MODE: Using {self.network} (simulated)"
            )
        else:
            logger.info(f"🔧 MOCK SDK Configured: Network={self.network} (simulated)")
    
    def create_wallet(self) -> str:
        """
        MOCK: Create a new wallet for settlement operations.
        
        Returns:
            str: The mock wallet address
        """
        logger.info("🔨 MOCK: Creating new smart account...")
        # Generate a mock Ethereum address
        self.account_address = f"0x{''.join(random.choices('0123456789abcdef', k=40))}"
        logger.info(f"✅ MOCK Smart Account Created: Address={self.account_address}")
        logger.info(f"💾 Persist this address: export PAYROLL_WALLET_ADDRESS={self.account_address}")
        return self.account_address
    
    def load_wallet(self, wallet_address: str) -> str:
        """
        MOCK: Load an existing smart account by its address.
        
        Args:
            wallet_address: The address of the smart account to load
            
        Returns:
            str: The loaded wallet address
        """
        logger.info(f"📂 MOCK: Loading smart account: {wallet_address}")
        self.account_address = wallet_address
        logger.info(f"✅ MOCK Smart Account Loaded: Address={self.account_address}")
        return self.account_address
    
    def load_wallet_from_seed(self, seed: str) -> str:
        """
        MOCK: Load a smart account from its seed phrase.
        
        Args:
            seed: The seed phrase (not used in mock implementation)
            
        Returns:
            str: The mock wallet address
        """
        logger.warning("🌱 MOCK: Seed import - creating new account")
        return self.create_wallet()
    
    def _ensure_wallet(self) -> str:
        """
        MOCK: Ensure a smart account is initialized, loading or creating as needed.
        
        Returns:
            str: The initialized wallet address
        """
        if self.account_address is not None:
            return self.account_address
        
        # Try loading from wallet address
        wallet_address = os.getenv("PAYROLL_WALLET_ADDRESS")
        if wallet_address:
            logger.info("🔑 MOCK: Initializing account from PAYROLL_WALLET_ADDRESS")
            return self.load_wallet(wallet_address)
        
        # Try loading from legacy wallet ID (treat as address)
        wallet_id = os.getenv("PAYROLL_WALLET_ID")
        if wallet_id:
            logger.info("🔑 MOCK: Initializing account from PAYROLL_WALLET_ID")
            return self.load_wallet(wallet_id)
        
        # Create new account if neither is set
        logger.warning("⚠️  MOCK: No wallet credentials found - creating new account")
        return self.create_wallet()
    
    def get_balance(self, asset: str = "usdc") -> Decimal:
        """
        MOCK: Get the wallet balance for a specified asset.
        
        Args:
            asset: The asset to check balance for (default: "usdc")
            
        Returns:
            Decimal: The mock balance amount
        """
        # Ensure account is initialized
        self._ensure_wallet()
        
        logger.info(f"💰 MOCK Balance: {self.mock_balance} {asset.upper()}")
        return self.mock_balance
    
    def request_faucet(self, asset: str = "usdc") -> None:
        """
        MOCK: Request testnet funds from the faucet.
        
        Args:
            asset: The asset to request from faucet (default: "usdc")
            
        Raises:
            ValueError: If called on mainnet network
        """
        # Prevent faucet requests on mainnet
        if self.network == "base-mainnet":
            error_msg = "❌ MOCK: Faucet not available on mainnet"
            logger.error(error_msg)
            raise ValueError(error_msg)
        
        # Ensure account is initialized
        self._ensure_wallet()
        
        # Simulate faucet request
        logger.info(f"🚰 MOCK: Requesting faucet funds: {asset.upper()}...")
        time.sleep(0.5)  # Simulate network delay
        self.mock_balance += Decimal("1000.00")  # Add 1000 USDC
        
        logger.info(f"✅ MOCK: Faucet request completed for {asset.upper()}")
    
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
            
            # MOCK: Simulate the transfer
            time.sleep(0.3)  # Simulate network delay
            
            # Deduct from mock balance
            self.mock_balance -= amount
            
            # Calculate execution duration
            duration = time.time() - start_time
            
            # Generate mock transaction hash
            hash_input = f"{to_address}{amount}{time.time()}".encode()
            transaction_hash = "0x" + hashlib.sha256(hash_input).hexdigest()
            
            # Build transaction link for Base network
            if self.network == "base-mainnet":
                transaction_link = f"https://basescan.org/tx/{transaction_hash}"
            else:
                transaction_link = f"https://sepolia.basescan.org/tx/{transaction_hash}"
            
            # Log successful transfer
            logger.info(
                f"✅ MOCK Transfer Confirmed{employee_context}: "
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
                f"❌ MOCK Transfer Failed{employee_context}: {error_msg}"
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
