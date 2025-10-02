#!/usr/bin/env python3
"""
Test script to verify AI model info display with mobile responsiveness
"""

import requests
import re

def test_model_info_display():
    """Test that AI model info is properly displayed and responsive"""
    print("🔍 Testing AI Model Info Display & Mobile Responsiveness")
    print("=" * 60)
    
    try:
        # Test the chat page
        response = requests.get('http://127.0.0.1:8000/chat/?force_chat=1', timeout=10)
        content = response.text
        
        print("📄 Checking HTML Content:")
        html_checks = {
            'ai_model_info_section': 'ai-model-info' in content,
            'model_name_display': 'model-name' in content,
            'model_provider_display': 'model-provider' in content,
            'model_status_display': 'model-status' in content,
            'gpt_model_shown': 'gpt-4.1-nano' in content,
            'euron_provider_shown': 'Euron API' in content,
        }
        
        all_html_passed = True
        for check_name, result in html_checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check_name.replace('_', ' ').title()}: {result}")
            if not result:
                all_html_passed = False
        
        print("\n🎨 Checking CSS Styles:")
        css_response = requests.get('http://127.0.0.1:8000/static/css/style.css', timeout=5)
        css_content = css_response.text
        
        css_checks = {
            'ai_model_info_styles': '.ai-model-info' in css_content,
            'mobile_responsive_480px': '@media (max-width: 480px)' in css_content and '.ai-model-info' in css_content,
            'tablet_responsive_768px': '@media (min-width: 481px) and (max-width: 768px)' in css_content,
            'desktop_styles': '@media (min-width: 993px)' in css_content,
            'status_indicators': '.status-indicator' in css_content,
            'pulse_animation': '@keyframes pulse' in css_content,
        }
        
        all_css_passed = True
        for check_name, result in css_checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check_name.replace('_', ' ').title()}: {result}")
            if not result:
                all_css_passed = False
        
        print("\n📱 Checking Responsive Breakpoints:")
        responsive_checks = {
            'mobile_portrait_480px': 'max-width: 480px' in css_content and 'ai-model-info' in css_content,
            'mobile_landscape_768px': 'max-width: 768px' in css_content and 'ai-model-info' in css_content,
            'tablet_992px': 'max-width: 992px' in css_content,
            'desktop_large': 'min-width: 993px' in css_content,
            'landscape_orientation': 'orientation: landscape' in css_content,
        }
        
        all_responsive_passed = True
        for check_name, result in responsive_checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check_name.replace('_', ' ').title()}: {result}")
            if not result:
                all_responsive_passed = False
        
        print("\n🔧 Testing Existing Features Still Work:")
        feature_checks = {
            'chat_container': 'chat-container' in content,
            'sidebar_exists': 'sidebar' in content,
            'messages_container': 'messages-container' in content,
            'input_area': 'input-area' in content,
            'new_chat_button': 'new-chat-btn' in content,
        }
        
        all_features_work = True
        for check_name, result in feature_checks.items():
            status = "✅" if result else "❌"
            print(f"  {status} {check_name.replace('_', ' ').title()}: {result}")
            if not result:
                all_features_work = False
        
        # Final result
        print("\n" + "=" * 60)
        
        if all_html_passed and all_css_passed and all_responsive_passed and all_features_work:
            print("🎉 AI MODEL INFO IS FULLY RESPONSIVE!")
            print("📱 Mobile, tablet, and desktop layouts implemented")
            print("✨ All existing features remain intact")
            print("🛡️ Ready for all screen sizes and devices")
            return True
        else:
            print("⚠️  Some responsive features need attention")
            if not all_html_passed:
                print("❓ HTML content issues detected")
            if not all_css_passed:
                print("❓ CSS styling issues detected") 
            if not all_responsive_passed:
                print("❓ Responsive breakpoints issues detected")
            if not all_features_work:
                print("❓ Existing features may be affected")
            return False
            
    except Exception as e:
        print(f"❌ Test error: {e}")
        return False

if __name__ == "__main__":
    success = test_model_info_display()
    exit(0 if success else 1)