#!/usr/bin/env python3
"""
Quick development environment test
"""

import requests
import sys

def test_development_server():
    """Test if the development server is working properly"""
    
    print("🔍 Testing Development Server Functionality...")
    print("=" * 50)
    
    base_url = "http://localhost:8001"
    
    # Test 1: Health check (if available)
    try:
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health/", timeout=5)
        print(f"   Health check: {response.status_code}")
        if response.status_code == 200:
            print(f"   Response: {response.text[:100]}")
    except Exception as e:
        print(f"   Health check failed: {e}")
    
    # Test 2: Root URL
    try:
        print("\n2. Testing root URL (/)...")
        response = requests.get(base_url, timeout=5, allow_redirects=False)
        print(f"   Status: {response.status_code}")
        if response.status_code in [301, 302]:
            print(f"   Redirects to: {response.headers.get('Location', 'Unknown')}")
        else:
            print(f"   Content length: {len(response.content)} bytes")
    except Exception as e:
        print(f"   Root URL test failed: {e}")
    
    # Test 3: Chat URL (main app)
    try:
        print("\n3. Testing /chat/ (main app)...")
        response = requests.get(f"{base_url}/chat/", timeout=5, allow_redirects=False)
        print(f"   Status: {response.status_code}")
        if response.status_code in [301, 302]:
            print(f"   Redirects to: {response.headers.get('Location', 'Unknown')}")
        elif response.status_code == 200:
            content = response.text
            print(f"   Content length: {len(content)} bytes")
            if "Login" in content:
                print("   ⚠️  Shows login page (authentication required)")
            elif "Hackversity" in content:
                print("   ✅ Shows main Hackversity page")
            elif "Chat" in content:
                print("   ✅ Shows chat interface")
        else:
            print(f"   Unexpected status: {response.status_code}")
    except Exception as e:
        print(f"   Chat URL test failed: {e}")
    
    # Test 4: Login page
    try:
        print("\n4. Testing login page...")
        response = requests.get(f"{base_url}/accounts/login/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   Login page loads: ✅")
            if "Sign In" in response.text or "Login" in response.text:
                print("   Contains login form: ✅")
        else:
            print(f"   Login page issue: {response.status_code}")
    except Exception as e:
        print(f"   Login page test failed: {e}")
    
    # Test 5: Static files
    try:
        print("\n5. Testing static files...")
        response = requests.get(f"{base_url}/static/css/style.css", timeout=5)
        print(f"   CSS file status: {response.status_code}")
        
        response = requests.get(f"{base_url}/static/js/chat.js", timeout=5)
        print(f"   JS file status: {response.status_code}")
        
        if response.status_code == 200:
            print("   Static files loading: ✅")
        else:
            print("   Static files issue: ⚠️")
    except Exception as e:
        print(f"   Static files test failed: {e}")
    
    print("\n" + "=" * 50)
    print("Development test complete!")
    
    print("\n📋 What to check:")
    print("1. If you see 302 redirects to /accounts/login/, you need to log in")
    print("2. If static files fail, run: python manage.py collectstatic")
    print("3. If login page loads but looks broken, check template/CSS issues")
    print("4. If everything redirects to login, authentication is working correctly")

if __name__ == "__main__":
    test_development_server()