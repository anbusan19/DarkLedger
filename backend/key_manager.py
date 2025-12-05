"""
Key Manager for Coinbase CDP Credentials

Securely loads API credentials from environment variables.
Never hardcode keys - this is THE BODY protecting THE BRAIN's secrets.
"""

import os
from typing import Tuple


class KeyManager:
    """Manages secure loading of Coinbase API credentials."""
    
    def __init__(self):
        """
        Initialize KeyManager by loading credentials from environment variables.
        
        Raises:
            ValueError: If either COINBASE_API_KEY_NAME or COINBASE_PRIVATE_KEY is missing
        """
        self.api_key_name = os.getenv("COINBASE_API_KEY_NAME")
        self.private_key = os.getenv("COINBASE_PRIVATE_KEY")
        
        if not self.api_key_name or not self.private_key:
            raise ValueError(
                "Missing required environment variables: "
                "COINBASE_API_KEY_NAME and COINBASE_PRIVATE_KEY must be set"
            )
    
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
