#!/usr/bin/env python3
"""
Responsive Design Test Suite for Hackversity
Tests various viewport sizes and device types
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from django.test import Client
from django.contrib.auth import get_user_model

def test_responsive_design():
    """Test responsive design across different viewport sizes"""
    print("🔍 Testing Responsive Design Across All Device Types")
    print("=" * 60)
    
    client = Client()
    User = get_user_model()
    
    # Create test user
    test_user = User.objects.create_user(
        username='responsive_tester',
        email='test@example.com',
        password='testpass123'
    )
    
    # Test different viewport sizes
    viewports = [
        {"name": "Mobile Portrait (iPhone SE)", "width": 375, "height": 667},
        {"name": "Mobile Portrait (iPhone 12)", "width": 390, "height": 844},
        {"name": "Mobile Landscape (iPhone SE)", "width": 667, "height": 375},
        {"name": "Mobile Large (iPhone 12 Pro Max)", "width": 428, "height": 926},
        {"name": "Tablet Portrait (iPad)", "width": 768, "height": 1024},
        {"name": "Tablet Landscape (iPad)", "width": 1024, "height": 768},
        {"name": "Small Desktop", "width": 1200, "height": 800},
        {"name": "Large Desktop", "width": 1920, "height": 1080},
        {"name": "Ultra Wide", "width": 2560, "height": 1440}
    ]
    
    pages_to_test = [
        {'url': '/', 'name': 'Home Page'},
        {'url': '/accounts/login/', 'name': 'Login Page'},
        {'url': '/accounts/signup/', 'name': 'Signup Page'},
        {'url': '/chat/', 'name': 'Chat Page'}
    ]
    
    # Test each viewport size
    for viewport in viewports:
        print(f"\n📱 Testing {viewport['name']} ({viewport['width']}x{viewport['height']})")
        print("-" * 50)
        
        # Set viewport headers (simulated)
        headers = {
            'HTTP_USER_AGENT': f'Mozilla/5.0 (compatible; ResponsiveTest/{viewport["width"]}x{viewport["height"]})',
            'HTTP_VIEWPORT_WIDTH': str(viewport['width']),
            'HTTP_VIEWPORT_HEIGHT': str(viewport['height'])
        }
        
        for page in pages_to_test:
            try:
                response = client.get(page['url'], **headers)
                status = "✅ OK" if response.status_code in [200, 302] else f"❌ {response.status_code}"
                
                # Check for responsive elements in content
                content = response.content.decode('utf-8') if hasattr(response, 'content') else ""
                
                responsive_indicators = {
                    'Viewport Meta': 'viewport' in content and 'width=device-width' in content,
                    'Responsive CSS': 'responsive.css' in content or '@media' in content,
                    'Mobile Friendly': 'touch' in content.lower() or 'mobile' in content.lower(),
                    'Font Awesome': 'font-awesome' in content or 'fa-' in content
                }
                
                print(f"   {page['name']:<15} {status}")
                
                # Show responsive indicators for first few viewports
                if viewport['width'] <= 768:  # Mobile viewports
                    indicators_status = " | ".join([
                        f"{k}: {'✅' if v else '❌'}" for k, v in responsive_indicators.items()
                    ])
                    print(f"     Responsive Features: {indicators_status}")
                
            except Exception as e:
                print(f"   {page['name']:<15} ❌ Error: {str(e)[:50]}")
    
    # Test responsive breakpoints
    print(f"\n🎯 Testing CSS Breakpoints")
    print("-" * 30)
    
    breakpoints = [
        {"name": "Extra Small", "max_width": 480, "description": "Mobile phones (portrait)"},
        {"name": "Small", "min_width": 481, "max_width": 768, "description": "Mobile phones (landscape) & small tablets"},
        {"name": "Medium", "min_width": 769, "max_width": 992, "description": "Tablets"},
        {"name": "Large", "min_width": 993, "max_width": 1200, "description": "Small desktops"},
        {"name": "Extra Large", "min_width": 1201, "description": "Large desktops"}
    ]
    
    for breakpoint in breakpoints:
        print(f"   {breakpoint['name']:<12} | {breakpoint['description']}")
        if 'max_width' in breakpoint:
            print(f"   {'Range:':<12} | {breakpoint.get('min_width', 0)}px - {breakpoint['max_width']}px")
        else:
            print(f"   {'Range:':<12} | {breakpoint['min_width']}px+")
    
    # Check for responsive features in static files
    print(f"\n📊 Static Files Analysis")
    print("-" * 25)
    
    static_files_to_check = [
        'static/css/style.css',
        'static/js/responsive.js',
        'static/js/chat.js'
    ]
    
    for file_path in static_files_to_check:
        try:
            full_path = os.path.join(os.getcwd(), file_path)
            if os.path.exists(full_path):
                with open(full_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    
                responsive_features = {
                    'Media Queries': content.count('@media'),
                    'Viewport Units': content.count('vw') + content.count('vh'),
                    'Flexbox': content.count('flex'),
                    'Grid': content.count('grid'),
                    'Clamp Functions': content.count('clamp('),
                    'Touch Events': content.count('touch'),
                }
                
                print(f"   {os.path.basename(file_path):<20} | Size: {len(content):,} chars")
                for feature, count in responsive_features.items():
                    if count > 0:
                        print(f"   {'':<20} | {feature}: {count}")
            else:
                print(f"   {os.path.basename(file_path):<20} | ❌ Not found")
                
        except Exception as e:
            print(f"   {os.path.basename(file_path):<20} | ❌ Error reading file")
    
    # Performance recommendations
    print(f"\n⚡ Performance & Accessibility Recommendations")
    print("-" * 45)
    
    recommendations = [
        "✅ Use viewport meta tag for proper mobile scaling",
        "✅ Implement touch-friendly button sizes (min 44px)",
        "✅ Use relative units (rem, em, %) for scalable layouts",
        "✅ Optimize images with responsive loading",
        "✅ Implement proper focus states for keyboard navigation",
        "✅ Use media queries for device-specific optimizations",
        "✅ Test on real devices, not just browser dev tools",
        "✅ Ensure text remains readable when zoomed to 200%",
        "✅ Implement swipe gestures for mobile navigation",
        "✅ Use CSS Grid and Flexbox for flexible layouts"
    ]
    
    for rec in recommendations:
        print(f"   {rec}")
    
    # Clean up
    test_user.delete()
    
    print(f"\n🎉 Responsive Design Testing Complete!")
    print("=" * 60)
    
    # Device testing checklist
    print(f"\n📋 Manual Testing Checklist")
    print("-" * 25)
    devices_to_test = [
        "📱 iPhone SE (375x667)",
        "📱 iPhone 12 Pro (390x844)",
        "📱 Samsung Galaxy S21 (360x800)",
        "📱 iPad Mini (768x1024)",
        "💻 iPad Pro (1024x1366)",
        "💻 MacBook Air (1440x900)",
        "🖥️  Desktop 1080p (1920x1080)",
        "🖥️  4K Monitor (3840x2160)"
    ]
    
    for device in devices_to_test:
        print(f"   □ {device}")
    
    print(f"\n💡 Next Steps:")
    print("   1. Test on actual mobile devices")
    print("   2. Validate touch interactions")
    print("   3. Check loading performance on slow networks")
    print("   4. Verify accessibility with screen readers")
    print("   5. Test keyboard navigation")

if __name__ == "__main__":
    test_responsive_design()