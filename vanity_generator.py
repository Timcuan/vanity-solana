import base58
import secrets
from typing import Tuple, Optional
from solana.keypair import Keypair
from solana.publickey import PublicKey
import time
from config import SOLANA_NETWORK

class SolanaVanityGenerator:
    def __init__(self, max_attempts: int = 1000000):
        self.max_attempts = max_attempts
    
    def generate_vanity_address(self, prefix: str) -> Tuple[Optional[Keypair], int, float]:
        """
        Generate a Solana vanity address with the specified prefix.
        
        Args:
            prefix (str): The desired prefix for the address
            
        Returns:
            Tuple[Optional[Keypair], int, float]: (keypair, attempts, time_taken)
        """
        if not prefix:
            return None, 0, 0.0
            
        prefix = prefix.upper()
        start_time = time.time()
        attempts = 0
        
        print(f"🔍 Searching for address starting with: {prefix}")
        
        while attempts < self.max_attempts:
            attempts += 1
            
            # Generate a new keypair
            keypair = Keypair()
            public_key = str(keypair.public_key)
            
            # Check if the address starts with the desired prefix
            if public_key.startswith(prefix):
                time_taken = time.time() - start_time
                print(f"✅ Found vanity address after {attempts:,} attempts in {time_taken:.2f} seconds")
                return keypair, attempts, time_taken
            
            # Progress update every 10000 attempts
            if attempts % 10000 == 0:
                elapsed = time.time() - start_time
                rate = attempts / elapsed if elapsed > 0 else 0
                print(f"⏳ Attempts: {attempts:,} | Rate: {rate:.0f}/sec | Elapsed: {elapsed:.1f}s")
        
        time_taken = time.time() - start_time
        print(f"❌ Failed to find vanity address after {attempts:,} attempts")
        return None, attempts, time_taken
    
    def validate_prefix(self, prefix: str) -> Tuple[bool, str]:
        """
        Validate the vanity address prefix.
        
        Args:
            prefix (str): The prefix to validate
            
        Returns:
            Tuple[bool, str]: (is_valid, error_message)
        """
        if not prefix:
            return False, "Prefix cannot be empty"
        
        if len(prefix) > 8:
            return False, "Prefix cannot be longer than 8 characters"
        
        # Check if prefix contains only valid characters (base58 alphabet)
        valid_chars = set("123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz")
        invalid_chars = set(prefix) - valid_chars
        
        if invalid_chars:
            return False, f"Invalid characters in prefix: {', '.join(invalid_chars)}"
        
        return True, ""
    
    def format_keypair_info(self, keypair: Keypair, attempts: int, time_taken: float) -> str:
        """
        Format keypair information for display.
        
        Args:
            keypair (Keypair): The generated keypair
            attempts (int): Number of attempts made
            time_taken (float): Time taken to generate
            
        Returns:
            str: Formatted keypair information
        """
        public_key = str(keypair.public_key)
        private_key = base58.b58encode(keypair.secret_key).decode('utf-8')
        
        info = f"""
🎯 **Vanity Address Generated Successfully!**

📊 **Generation Stats:**
• Attempts: {attempts:,}
• Time taken: {time_taken:.2f} seconds
• Rate: {attempts/time_taken:.0f} attempts/sec

🔑 **Public Key:**
`{public_key}`

🔐 **Private Key:**
`{private_key}`

⚠️ **Security Warning:**
• Keep your private key secure and never share it
• This is a real Solana keypair that can hold funds
• Store the private key offline in a secure location
• Consider using a hardware wallet for large amounts

🌐 **Network:** Solana {SOLANA_NETWORK}
"""
        return info
    
    def estimate_generation_time(self, prefix: str) -> str:
        """
        Estimate the time needed to generate a vanity address.
        
        Args:
            prefix (str): The desired prefix
            
        Returns:
            str: Estimated time information
        """
        if not prefix:
            return "Invalid prefix"
        
        # Rough estimation based on prefix length
        # This is a simplified estimation
        length = len(prefix)
        
        if length <= 2:
            return "~1-10 seconds"
        elif length == 3:
            return "~10-60 seconds"
        elif length == 4:
            return "~1-10 minutes"
        elif length == 5:
            return "~10-60 minutes"
        elif length == 6:
            return "~1-10 hours"
        elif length == 7:
            return "~10-100 hours"
        else:  # length == 8
            return "~100+ hours (very long)"