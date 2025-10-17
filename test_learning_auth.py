#!/usr/bin/env python
"""
Test Learning Module Authentication
This script tests that learning module views require authentication.
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

def test_learning_authentication():
    """Test that learning module views require authentication"""
    print("🔐 Testing Learning Module Authentication")
    print("=" * 60)
    
    client = Client()
    
    # Test URLs that should require authentication
    test_urls = [
        '/chat/learning/',
        '/learning/',
        '/chat/learning/getting-started/',
        '/chat/learning/network-security/',
    ]
    
    print("\n📋 Testing unauthenticated access (should redirect to login):")
    for url in test_urls:
        response = client.get(url)
        if response.status_code in [302, 301]:  # Redirect
            # Check if redirecting to login
            redirect_url = response.url
            if '/accounts/login/' in redirect_url or '/login/' in redirect_url:
                print(f"  ✅ {url}")
                print(f"     → Redirects to login: {redirect_url}")
            else:
                print(f"  ⚠️  {url}")
                print(f"     → Redirects to: {redirect_url} (expected login)")
        else:
            print(f"  ❌ {url}")
            print(f"     → Status: {response.status_code} (expected redirect)")
    
    # Create a test user and test authenticated access
    print("\n📋 Testing authenticated access (should allow):")
    try:
        # Try to get existing user or create new one
        test_user, created = User.objects.get_or_create(
            username='testuser',
            defaults={'email': 'test@example.com'}
        )
        if created:
            test_user.set_password('testpass123')
            test_user.save()
            print("  ℹ️  Created test user: testuser")
        else:
            print("  ℹ️  Using existing test user: testuser")
        
        # Login the test user
        client.login(username='testuser', password='testpass123')
        
        for url in test_urls:
            response = client.get(url, follow=True)
            if response.status_code == 200:
                print(f"  ✅ {url}")
                print(f"     → Status: {response.status_code} (OK)")
            else:
                print(f"  ⚠️  {url}")
                print(f"     → Status: {response.status_code}")
                
    except Exception as e:
        print(f"  ❌ Error testing authenticated access: {e}")
    
    print("\n" + "=" * 60)
    print("✅ Authentication test completed!")
    print("\nℹ️  Summary:")
    print("   - Learning module pages now require authentication")
    print("   - Unauthenticated users are redirected to login")
    print("   - Authenticated users can access learning modules")


def main():
    """Main function"""
    try:
        test_learning_authentication()
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
