"""
Key Manager for Coinbase CDP Credentials

Returns mock credentials when API keys are not provided.
Works without API keys - system automatically falls back to mock mode.
Never hardcode keys - this is THE BODY protecting THE BRAIN's secrets.
"""

import os
from typing import Tuple


class KeyManager:
    """Manages secure loading of Coinbase API credentials (optional)."""
    
    def __init__(self):
        """
        Initialize KeyManager with credentials from environment or mock values.
        
        API keys are optional. If not provided, system uses mock values.
        Environment variables supported:
        - CDP_API_KEY_ID and CDP_API_KEY_SECRET (new SDK format)
        - COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY (legacy format)
        
        If neither is set, uses mock credentials for testing.
        """
        # Try to load from environment, fallback to mock values if not present
        self.api_key_name = os.getenv("CDP_API_KEY_ID") or os.getenv("COINBASE_API_KEY_NAME") or "MOCK_API_KEY"
        self.private_key = os.getenv("CDP_API_KEY_SECRET") or os.getenv("COINBASE_PRIVATE_KEY") or "MOCK_PRIVATE_KEY"
        self.is_mock = not (os.getenv("CDP_API_KEY_ID") or os.getenv("COINBASE_API_KEY_NAME"))
    
    def get_credentials(self) -> Tuple[str, str]:
        """
        Returns the API credentials as a tuple.
        
        Returns:
            Tuple[str, str]: (api_key_name, private_key)
        """
        return self.api_key_name, self.private_key
    
    def __repr__(self) -> str:
        """
        String representation that masks credentials in logs.
        Never expose actual keys in logs or debug output.
        
        Returns:
            str: Masked representation of KeyManager
        """
        api_key_status = "***" if self.api_key_name else "None"
        private_key_status = "***" if self.private_key else "None"
        return f"KeyManager(api_key_name={api_key_status}, private_key={private_key_status})"


# Singleton instance - initialize once at module level
key_manager = KeyManager()
