#!/usr/bin/env python
"""
Development Test Suite
Quick tests to verify the development environment is working correctly.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

def test_database_connection():
    """Test if database connection is working"""
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT 1")
        result = cursor.fetchone()
        print("✅ Database connection: OK")
        return True
    except Exception as e:
        print(f"❌ Database connection: FAILED - {e}")
        return False

def test_models():
    """Test if models can be imported and basic operations work"""
    try:
        from accounts.models import CustomUser
        from chat.models import Conversation, Message
        
        # Test model imports
        print("✅ Models import: OK")
        
        # Test basic query (should not fail even if no data)
        user_count = CustomUser.objects.count()
        conv_count = Conversation.objects.count()
        msg_count = Message.objects.count()
        
        print(f"📊 Database stats: {user_count} users, {conv_count} conversations, {msg_count} messages")
        return True
    except Exception as e:
        print(f"❌ Models test: FAILED - {e}")
        return False

def test_euron_api():
    """Test if Euron API key is configured"""
    try:
        from django.conf import settings
        api_key = getattr(settings, 'EURON_API_KEY', None)
        
        if api_key and api_key.startswith('euri-'):
            print("✅ Euron API key: Configured")
            
            # Try to import the service
            from chat.services import get_ai_response
            print("✅ Euron service import: OK")
            return True
        else:
            print("⚠️  Euron API key: Not configured or invalid format")
            return False
    except Exception as e:
        print(f"❌ Euron API test: FAILED - {e}")
        return False

def test_static_files():
    """Test if static files configuration is working"""
    try:
        from django.conf import settings
        from django.contrib.staticfiles.finders import find
        
        # Check static settings
        print(f"✅ Static URL: {settings.STATIC_URL}")
        print(f"✅ Static Root: {settings.STATIC_ROOT}")
        print(f"✅ Static Dirs: {settings.STATICFILES_DIRS}")
        
        return True
    except Exception as e:
        print(f"❌ Static files test: FAILED - {e}")
        return False

def test_urls():
    """Test if URL configuration is working"""
    try:
        from django.urls import reverse
        
        # Test basic URLs
        home_url = reverse('accounts:home')
        login_url = reverse('accounts:login')
        print(f"✅ URLs working: Home({home_url}), Login({login_url})")
        return True
    except Exception as e:
        print(f"❌ URLs test: FAILED - {e}")
        return False

def main():
    """Run all development tests"""
    print("🧪 Running Development Environment Tests")
    print("=" * 50)
    
    tests = [
        test_database_connection,
        test_models,
        test_euron_api,
        test_static_files,
        test_urls,
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        try:
            if test():
                passed += 1
        except Exception as e:
            print(f"❌ Test {test.__name__} crashed: {e}")
        print()
    
    print("=" * 50)
    print(f"🏁 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Development environment is ready.")
        print("\nNext steps:")
        print("1. Run: python manage.py runserver")
        print("2. Visit: http://127.0.0.1:8000")
        print("3. Register a user and test the chat feature")
    else:
        print("⚠️  Some tests failed. Check the output above for details.")
        
    return passed == total

if __name__ == '__main__':
    main()