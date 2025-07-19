#!/usr/bin/env python3
"""
Test script for the Solana Vanity Generator
Run this to test the generator functionality before using the bot.
"""

import time
from vanity_generator import SolanaVanityGenerator
from config import MAX_ATTEMPTS

def test_vanity_generator():
    """Test the vanity generator with different prefixes."""
    
    print("🧪 Testing Solana Vanity Generator")
    print("=" * 50)
    
    # Initialize generator
    generator = SolanaVanityGenerator(max_attempts=MAX_ATTEMPTS)
    
    # Test cases
    test_cases = [
        "A",      # Very short - should be fast
        "123",    # Short numeric - should be fast
        "SOL",    # Medium - should be moderate
        "TEST",   # Medium - should be moderate
    ]
    
    for prefix in test_cases:
        print(f"\n🔍 Testing prefix: '{prefix}'")
        print("-" * 30)
        
        # Validate prefix
        is_valid, error = generator.validate_prefix(prefix)
        if not is_valid:
            print(f"❌ Validation failed: {error}")
            continue
        
        print(f"✅ Prefix validated successfully")
        print(f"⏱️  Estimated time: {generator.estimate_generation_time(prefix)}")
        
        # Generate vanity address
        start_time = time.time()
        keypair, attempts, time_taken = generator.generate_vanity_address(prefix)
        
        if keypair:
            print(f"🎯 Success! Found address starting with '{prefix}'")
            print(f"📊 Attempts: {attempts:,}")
            print(f"⏱️  Time taken: {time_taken:.2f} seconds")
            print(f"🔑 Public Key: {str(keypair.public_key)}")
            print(f"🔐 Private Key: {str(keypair.secret_key.hex())}")
        else:
            print(f"❌ Failed to generate address with prefix '{prefix}'")
            print(f"📊 Attempts made: {attempts:,}")
            print(f"⏱️  Time spent: {time_taken:.2f} seconds")
        
        # Add delay between tests
        time.sleep(1)
    
    print("\n" + "=" * 50)
    print("✅ Test completed!")

def test_validation():
    """Test the validation function."""
    
    print("\n🔍 Testing Validation Function")
    print("=" * 50)
    
    generator = SolanaVanityGenerator()
    
    test_cases = [
        ("", "Empty prefix"),
        ("A", "Valid single character"),
        ("123", "Valid numeric"),
        ("SOL", "Valid alphabetic"),
        ("SOL123", "Valid alphanumeric"),
        ("SOL@123", "Invalid character @"),
        ("SOL 123", "Invalid space"),
        ("SOLANA123456789", "Too long"),
        ("SOL-123", "Invalid character -"),
    ]
    
    for prefix, description in test_cases:
        is_valid, error = generator.validate_prefix(prefix)
        status = "✅" if is_valid else "❌"
        print(f"{status} {description}: '{prefix}' - {error if not is_valid else 'Valid'}")

if __name__ == "__main__":
    print("🚀 Solana Vanity Generator Test Suite")
    print("This will test the generator functionality.")
    print("Note: This may take some time for longer prefixes.")
    
    # Test validation first
    test_validation()
    
    # Ask user if they want to run generation tests
    response = input("\nDo you want to run generation tests? (y/n): ").lower().strip()
    
    if response in ['y', 'yes']:
        test_vanity_generator()
    else:
        print("Skipping generation tests.")
    
    print("\n🎉 All tests completed!")