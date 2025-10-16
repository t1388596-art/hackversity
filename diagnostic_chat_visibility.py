"""
Chat Visibility Diagnostic Script
Checks for common issues that prevent chat messages from being visible
"""

import os
import django
import sys

# Setup Django environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model
from chat.models import Conversation, Message

User = get_user_model()

def check_chat_visibility():
    """Diagnostic checks for chat visibility issues"""
    
    print("🔍 Chat Visibility Diagnostic")
    print("=" * 50)
    
    # 1. Check if messages exist in database
    print("\n1. 📊 Database Check:")
    conversations = Conversation.objects.all()
    messages = Message.objects.all()
    print(f"   Conversations: {conversations.count()}")
    print(f"   Messages: {messages.count()}")
    
    if messages.exists():
        latest_message = messages.last()
        print(f"   Latest message: '{latest_message.content[:50]}...'")
        print(f"   From user: {latest_message.is_from_user}")
        print(f"   Created: {latest_message.created_at}")
    
    # 2. Check static files
    print("\n2. 📁 Static Files Check:")
    from django.conf import settings
    
    chat_js_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR, 'static', 'js', 'chat.js')
    chat_css_path = os.path.join(settings.STATIC_ROOT or settings.BASE_DIR, 'static', 'css', 'style.css')
    
    print(f"   chat.js exists: {os.path.exists(chat_js_path)} ({chat_js_path})")
    print(f"   style.css exists: {os.path.exists(chat_css_path)} ({chat_css_path})")
    
    # Alternative paths
    alt_chat_js = os.path.join(settings.BASE_DIR, 'static', 'js', 'chat.js')
    alt_css = os.path.join(settings.BASE_DIR, 'static', 'css', 'style.css')
    
    print(f"   chat.js (alt path): {os.path.exists(alt_chat_js)} ({alt_chat_js})")
    print(f"   style.css (alt path): {os.path.exists(alt_css)} ({alt_css})")
    
    # 3. Check template rendering
    print("\n3. 🎨 Template Check:")
    client = Client()
    
    # Get or create user
    user, created = User.objects.get_or_create(
        email='test@hackversity.com',
        defaults={'username': 'testuser'}
    )
    
    client.force_login(user)
    
    try:
        response = client.get('/chat/')
        print(f"   Chat page status: {response.status_code}")
        
        if response.status_code == 200:
            content = response.content.decode('utf-8')
            
            # Check for key elements
            checks = [
                ('Messages Container', 'id="messagesContainer"' in content),
                ('Chat Form', 'id="chatForm"' in content),
                ('Message Input', 'id="messageInput"' in content),
                ('Chat.js Script', 'chat.js' in content),
                ('Send Button', 'sendButton' in content),
                ('CSRF Token', 'csrfmiddlewaretoken' in content),
            ]
            
            for check_name, result in checks:
                print(f"   {check_name}: {'✅' if result else '❌'}")
            
        else:
            print(f"   ❌ Template error: Status {response.status_code}")
            
    except Exception as e:
        print(f"   ❌ Template error: {e}")
    
    # 4. Check API endpoints
    print("\n4. 🔌 API Endpoints Check:")
    
    from django.urls import reverse
    
    try:
        send_url = reverse('chat:send_message')
        print(f"   Send message URL: {send_url} ✅")
    except Exception as e:
        print(f"   Send message URL: ❌ {e}")
    
    # 5. Check CSS for visibility issues
    print("\n5. 🎨 CSS Visibility Check:")
    
    if os.path.exists(alt_css):
        with open(alt_css, 'r', encoding='utf-8') as f:
            css_content = f.read()
            
        # Check for common visibility issues
        visibility_issues = [
            ('display: none', 'display:none' in css_content or 'display: none' in css_content),
            ('visibility: hidden', 'visibility:hidden' in css_content or 'visibility: hidden' in css_content),
            ('opacity: 0', 'opacity:0' in css_content or 'opacity: 0' in css_content),
        ]
        
        for issue, found in visibility_issues:
            if found:
                print(f"   ⚠️  Found potential issue: {issue}")
            else:
                print(f"   ✅ No {issue} issues")
    
    # 6. JavaScript function check
    print("\n6. 📜 JavaScript Functions Check:")
    
    if os.path.exists(alt_chat_js):
        with open(alt_chat_js, 'r', encoding='utf-8') as f:
            js_content = f.read()
        
        functions = ['sendMessage', 'addMessage', 'handleSubmit', 'initializeChat']
        
        for func in functions:
            if f'function {func}' in js_content:
                print(f"   ✅ {func} function exists")
            else:
                print(f"   ❌ {func} function missing")
    
    print("\n" + "=" * 50)
    print("🎯 Diagnostic Complete!")
    
    # Recommendations
    print("\n💡 Recommendations:")
    print("1. Check browser console for JavaScript errors")
    print("2. Verify that you're logged in when testing")
    print("3. Try hard refresh (Ctrl+F5) to clear cache")
    print("4. Check network tab in browser dev tools for failed requests")

if __name__ == "__main__":
    check_chat_visibility()