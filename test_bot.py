#!/usr/bin/env python3
"""
Test script for Solana Vanity Wallet Telegram Bot
"""

import os
import sys
from dotenv import load_dotenv

def test_environment():
    """Test environment configuration"""
    print("🔍 Testing environment configuration...")
    
    # Load environment variables
    load_dotenv()
    
    # Check required variables
    telegram_token = os.getenv('TELEGRAM_TOKEN')
    solana_network = os.getenv('SOLANA_NETWORK', 'mainnet-beta')
    max_attempts = os.getenv('MAX_ATTEMPTS', '1000000')
    max_prefix_length = os.getenv('MAX_PREFIX_LENGTH', '8')
    
    print(f"✅ TELEGRAM_TOKEN: {'Set' if telegram_token else 'Not set'}")
    print(f"✅ SOLANA_NETWORK: {solana_network}")
    print(f"✅ MAX_ATTEMPTS: {max_attempts}")
    print(f"✅ MAX_PREFIX_LENGTH: {max_prefix_length}")
    
    if not telegram_token:
        print("❌ Error: TELEGRAM_TOKEN not found in .env file")
        return False
    
    return True

def test_dependencies():
    """Test required dependencies"""
    print("\n�� Testing dependencies...")
    
    try:
        import telegram
        print("✅ python-telegram-bot imported successfully")
    except ImportError as e:
        print(f"❌ Error importing python-telegram-bot: {e}")
        return False
    
    try:
        import solders
        print("✅ solders imported successfully")
    except ImportError as e:
        print(f"❌ Error importing solders: {e}")
        return False
    
    try:
        import base58
        print("✅ base58 imported successfully")
    except ImportError as e:
        print(f"❌ Error importing base58: {e}")
        return False
    
    try:
        import dotenv
        print("✅ python-dotenv imported successfully")
    except ImportError as e:
        print(f"❌ Error importing python-dotenv: {e}")
        return False
    
    return True

def test_vanity_generator():
    """Test vanity generator functionality"""
    print("\n🔍 Testing vanity generator...")
    
    try:
        from vanity_generator import SolanaVanityGenerator
        
        # Create generator instance
        generator = SolanaVanityGenerator(max_attempts=1000)
        print("✅ SolanaVanityGenerator created successfully")
        
        # Test prefix validation
        is_valid, error = generator.validate_prefix("ABC")
        if is_valid:
            print("✅ Prefix validation working")
        else:
            print(f"❌ Prefix validation failed: {error}")
            return False
        
        # Test invalid prefix
        is_valid, error = generator.validate_prefix("ABC0")
        if not is_valid:
            print("✅ Invalid prefix detection working")
        else:
            print("❌ Invalid prefix detection failed")
            return False
        
        # Test time estimation
        time_est = generator.estimate_generation_time("ABC")
        print(f"✅ Time estimation working: {time_est}")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing vanity generator: {e}")
        return False

def test_bot_module():
    """Test bot module imports"""
    print("\n🔍 Testing bot module...")
    
    try:
        from bot import start_command, generate_command, help_command, status_command
        print("✅ Bot command handlers imported successfully")
        
        from bot import main
        print("✅ Bot main function imported successfully")
        
        return True
        
    except Exception as e:
        print(f"❌ Error testing bot module: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Solana Vanity Wallet Telegram Bot - Test Suite")
    print("=" * 50)
    
    tests = [
        ("Environment Configuration", test_environment),
        ("Dependencies", test_dependencies),
        ("Vanity Generator", test_vanity_generator),
        ("Bot Module", test_bot_module),
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        print(f"\n📋 Running: {test_name}")
        try:
            if test_func():
                print(f"✅ {test_name}: PASSED")
                passed += 1
            else:
                print(f"❌ {test_name}: FAILED")
        except Exception as e:
            print(f"❌ {test_name}: ERROR - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Bot is ready to deploy.")
        print("\n🚀 To start the bot, run:")
        print("   python3 bot.py")
        print("   or")
        print("   ./deploy_bot.sh")
        return True
    else:
        print("❌ Some tests failed. Please fix the issues before deploying.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
