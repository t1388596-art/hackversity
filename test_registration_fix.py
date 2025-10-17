#!/usr/bin/env python
"""
Test Registration Fix
This script tests that user registration works correctly with multiple authentication backends.
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

from django.test import Client
from django.contrib.auth import get_user_model

User = get_user_model()

def test_registration():
    """Test that registration works with multiple authentication backends"""
    print("🔐 Testing User Registration with Multiple Auth Backends")
    print("=" * 60)
    
    client = Client()
    
    # Clean up test user if exists
    test_username = f'testuser_{os.getpid()}'
    User.objects.filter(username=test_username).delete()
    
    print(f"\n📝 Testing registration for user: {test_username}")
    
    # Test registration
    registration_data = {
        'username': test_username,
        'email': f'{test_username}@test.com',
        'password1': 'testpass123!@#',
        'password2': 'testpass123!@#',
    }
    
    print("\n🔄 Submitting registration form...")
    response = client.post('/accounts/signup/', registration_data, follow=True)
    
    if response.status_code == 200:
        # Check if user was created
        try:
            user = User.objects.get(username=test_username)
            print(f"✅ User created successfully!")
            print(f"   Username: {user.username}")
            print(f"   Email: {user.email}")
            print(f"   Is Active: {user.is_active}")
            
            # Check if user is logged in
            if '_auth_user_id' in client.session:
                print(f"✅ User automatically logged in after registration")
            else:
                print(f"⚠️  User not automatically logged in")
            
            # Clean up
            user.delete()
            print(f"\n🧹 Test user cleaned up")
            
            return True
        except User.DoesNotExist:
            print(f"❌ User was not created")
            print(f"   Response status: {response.status_code}")
            if hasattr(response, 'content'):
                content = response.content.decode('utf-8')
                if 'error' in content.lower():
                    print(f"   Errors found in response")
            return False
    else:
        print(f"❌ Registration failed")
        print(f"   Status code: {response.status_code}")
        return False


def test_login():
    """Test that login works with multiple authentication backends"""
    print("\n\n🔐 Testing User Login with Multiple Auth Backends")
    print("=" * 60)
    
    client = Client()
    
    # Create a test user
    test_username = f'logintest_{os.getpid()}'
    User.objects.filter(username=test_username).delete()
    
    user = User.objects.create_user(
        username=test_username,
        email=f'{test_username}@test.com',
        password='testpass123'
    )
    
    print(f"\n📝 Testing login for user: {test_username}")
    
    # Test login
    login_data = {
        'username': test_username,
        'password': 'testpass123',
    }
    
    print("\n🔄 Submitting login form...")
    response = client.post('/accounts/login/', login_data, follow=True)
    
    if '_auth_user_id' in client.session:
        print(f"✅ User logged in successfully!")
        print(f"   Session user ID: {client.session['_auth_user_id']}")
        
        # Clean up
        user.delete()
        print(f"\n🧹 Test user cleaned up")
        return True
    else:
        print(f"❌ Login failed")
        print(f"   Status code: {response.status_code}")
        user.delete()
        return False


def check_auth_backends():
    """Check authentication backends configuration"""
    from django.conf import settings
    
    print("\n\n⚙️  Checking Authentication Backends Configuration")
    print("=" * 60)
    
    backends = settings.AUTHENTICATION_BACKENDS
    print(f"\n📋 Configured backends ({len(backends)}):")
    for i, backend in enumerate(backends, 1):
        print(f"   {i}. {backend}")
    
    if len(backends) > 1:
        print(f"\n✅ Multiple backends configured (requires explicit backend parameter)")
    else:
        print(f"\n✅ Single backend configured")


def main():
    """Main function"""
    try:
        check_auth_backends()
        
        registration_success = test_registration()
        login_success = test_login()
        
        print("\n" + "=" * 60)
        print("📊 Test Results:")
        print(f"   Registration: {'✅ PASSED' if registration_success else '❌ FAILED'}")
        print(f"   Login: {'✅ PASSED' if login_success else '❌ FAILED'}")
        
        if registration_success and login_success:
            print("\n✅ All tests passed! Registration issue is fixed.")
            return True
        else:
            print("\n⚠️  Some tests failed. Please check the output above.")
            return False
            
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
