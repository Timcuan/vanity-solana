#!/usr/bin/env python3
"""
Demo script for Solana Vanity Generator Mini App
"""

from vanity_generator import SolanaVanityGenerator
import time

def demo_vanity_generation():
    """Demo the vanity address generation"""
    print("🚀 Solana Vanity Generator Demo")
    print("=" * 40)
    
    # Initialize generator
    generator = SolanaVanityGenerator(max_attempts=10000)
    
    # Test prefix validation
    print("\n🔍 Testing prefix validation:")
    test_prefixes = ["SOL", "123", "ABC", "INVALID!", "TOOLONG123"]
    
    for prefix in test_prefixes:
        is_valid, error = generator.validate_prefix(prefix)
        status = "✅ Valid" if is_valid else f"❌ Invalid: {error}"
        print(f"  {prefix}: {status}")
    
    # Test time estimation
    print("\n⏱️ Testing time estimation:")
    for prefix in ["A", "SOL", "1234", "SOLANA"]:
        time_est = generator.estimate_generation_time(prefix)
        print(f"  {prefix}: {time_est}")
    
    # Test actual generation (short prefix for demo)
    print("\n🎯 Testing actual generation (prefix: 'A'):")
    start_time = time.time()
    
    keypair, attempts, time_taken = generator.generate_vanity_address("A")
    
    if keypair:
        print(f"✅ Success! Found address starting with 'A'")
        print(f"📊 Attempts: {attempts:,}")
        print(f"⏱️ Time taken: {time_taken:.2f} seconds")
        print(f"🔑 Public Key: {str(keypair.pubkey())}")
        print(f"🔐 Private Key: {generator.format_private_key(keypair)}")
    else:
        print(f"❌ Failed to find address after {attempts:,} attempts")
    
    print("\n🎉 Demo completed!")

if __name__ == "__main__":
    demo_vanity_generation()
