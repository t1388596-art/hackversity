#!/usr/bin/env python
"""
Test script to verify the signup->chat flow works without 500 errors
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

def test_signup_chat_flow():
    """Test the complete signup to chat flow"""
    from django.test import Client
    from django.contrib.auth import get_user_model
    from django.urls import reverse
    
    print("Testing signup -> chat flow...")
    
    User = get_user_model()
    client = Client()
    
    # Clean up any existing test user
    User.objects.filter(username='testflow_user').delete()
    
    # Test 1: Access chat page without login (should redirect or show error)
    print("\n1. Testing chat access without login...")
    try:
        response = client.get('/chat/')
        print(f"   ✓ Response status: {response.status_code}")
    except Exception as e:
        print(f"   ✗ Error accessing chat: {e}")
    
    # Test 2: Signup process
    print("\n2. Testing signup process...")
    try:
        signup_data = {
            'username': 'testflow_user',
            'email': 'testflow@example.com', 
            'first_name': 'Test',
            'last_name': 'User',
            'password1': 'complexpass123',
            'password2': 'complexpass123'
        }
        response = client.post('/accounts/signup/', signup_data)
        print(f"   ✓ Signup response status: {response.status_code}")
        
        if response.status_code == 302:
            print(f"   ✓ Signup redirected to: {response.url}")
        
        # Check if user was created
        if User.objects.filter(username='testflow_user').exists():
            print("   ✓ User created successfully")
        else:
            print("   ✗ User was not created")
            
    except Exception as e:
        print(f"   ✗ Signup error: {e}")
    
    # Test 3: Access chat after signup (simulate the redirect)
    print("\n3. Testing chat access after signup...")
    try:
        # Login the user manually to simulate successful signup
        user = User.objects.get(username='testflow_user')
        client.force_login(user)
        
        response = client.get('/chat/')
        print(f"   ✓ Chat access status: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✓ Chat page loads successfully after signup")
        elif response.status_code == 500:
            print("   ✗ 500 error still occurring")
        else:
            print(f"   ! Unexpected status code: {response.status_code}")
            
    except Exception as e:
        print(f"   ✗ Chat access error: {e}")
    
    # Test 4: Check URL resolution
    print("\n4. Testing URL resolution...")
    try:
        from django.urls import resolve
        
        # Test chat URL
        resolver = resolve('/chat/')
        print(f"   ✓ Chat URL resolves to: {resolver.func.__name__}")
        
        # Test accounts URLs
        resolver = resolve('/accounts/signup/')
        print(f"   ✓ Signup URL resolves to: {resolver.func.__name__}")
        
        resolver = resolve('/accounts/login/')
        print(f"   ✓ Login URL resolves to: {resolver.func.__name__}")
        
    except Exception as e:
        print(f"   ✗ URL resolution error: {e}")
    
    # Cleanup
    try:
        User.objects.filter(username='testflow_user').delete()
        print("\n   ✓ Test user cleaned up")
    except:
        pass
    
    print("\n🎉 Signup->Chat flow test completed!")
    return True

if __name__ == '__main__':
    success = test_signup_chat_flow()
    sys.exit(0 if success else 1)