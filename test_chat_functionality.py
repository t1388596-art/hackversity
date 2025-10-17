"""
Quick chat functionality test
Tests the chat send_message endpoint directly
"""

import os
import django
import sys
import json

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from django.urls import reverse

User = get_user_model()

def test_chat_functionality():
    """Test chat functionality with a real user"""
    print("🧪 Testing Chat Functionality...")
    
    # Create test client
    client = Client()
    
    # Create or get test user
    user, created = User.objects.get_or_create(
        email='test@hackversity.com',
        defaults={
            'username': 'testuser',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        user.set_password('testpass123')
        user.save()
        print(f"✅ Created test user: {user.email}")
    else:
        print(f"✅ Using existing test user: {user.email}")
    
    # Login the user
    login_success = client.login(email='test@hackversity.com', password='testpass123')
    
    if login_success:
        print("✅ User logged in successfully")
    else:
        print("❌ Login failed")
        return False
    
    # Test accessing chat home page
    try:
        response = client.get('/chat/')
        print(f"✅ Chat home page accessible: Status {response.status_code}")
        
        if response.status_code != 200:
            print(f"❌ Chat page returned status {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing chat page: {e}")
        return False
    
    # Test sending a message via API
    try:
        send_url = reverse('chat:send_message')
        print(f"📡 Testing send message API at: {send_url}")
        
        message_data = {
            'message': 'Hello, this is a test message!',
            'conversation_id': None
        }
        
        response = client.post(
            send_url,
            data=json.dumps(message_data),
            content_type='application/json'
        )
        
        print(f"📤 Send message response status: {response.status_code}")
        
        if response.status_code == 200:
            response_data = response.json()
            if response_data.get('success'):
                print("✅ Message sent successfully!")
                print(f"🆔 Conversation ID: {response_data.get('conversation_id')}")
                print(f"👤 User message: {response_data.get('user_message', {}).get('content', 'N/A')}")
                print(f"🤖 AI response: {response_data.get('ai_message', {}).get('content', 'N/A')[:100]}...")
                return True
            else:
                print(f"❌ Message failed: {response_data.get('error', 'Unknown error')}")
                return False
        else:
            print(f"❌ API returned status {response.status_code}")
            try:
                error_data = response.json()
                print(f"❌ Error details: {error_data}")
            except:
                print(f"❌ Response content: {response.content}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing send message: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    try:
        success = test_chat_functionality()
        if success:
            print("\n🎉 Chat functionality is working correctly!")
            print("🌐 You can now use the chat interface at http://127.0.0.1:8000/chat/")
        else:
            print("\n❌ Chat functionality test failed!")
            print("🔧 Check the error messages above for debugging information.")
    except Exception as e:
        print(f"❌ Test script error: {e}")
        import traceback
        traceback.print_exc()