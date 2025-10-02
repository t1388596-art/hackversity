#!/usr/bin/env python3
"""
Test script for the Cybersecurity Preloader functionality
This script tests the preloader integration without affecting existing features
"""

import os
import sys
import django
import time
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).parent
sys.path.insert(0, str(project_dir))

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

def test_static_files():
    """Test that preloader static files exist and are accessible"""
    print("🔍 Testing Preloader Static Files...")
    
    # Check CSS file
    css_path = project_dir / 'static' / 'css' / 'preloader.css'
    if css_path.exists():
        print("✅ Preloader CSS file exists")
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if '.preloader' in content and '.security-scanner' in content:
                print("✅ Preloader CSS contains required classes")
            else:
                print("❌ Preloader CSS missing required classes")
    else:
        print("❌ Preloader CSS file not found")
    
    # Check JS file
    js_path = project_dir / 'static' / 'js' / 'preloader.js'
    if js_path.exists():
        print("✅ Preloader JS file exists")
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
            if 'CyberSecurityPreloader' in content and 'init()' in content:
                print("✅ Preloader JS contains required functionality")
            else:
                print("❌ Preloader JS missing required functionality")
    else:
        print("❌ Preloader JS file not found")

def test_template_integration():
    """Test that preloader is properly integrated into base template"""
    print("\n🔍 Testing Template Integration...")
    
    base_template = project_dir / 'templates' / 'base.html'
    if base_template.exists():
        print("✅ Base template exists")
        with open(base_template, 'r', encoding='utf-8') as f:
            content = f.read()
            
            checks = {
                'preloader.css': 'preloader.css' in content,
                'preloader.js': 'preloader.js' in content,
                'proper_order': content.find('preloader.css') < content.find('</head>'),
                'js_before_body': content.find('preloader.js') < content.find('</body>')
            }
            
            for check_name, result in checks.items():
                if result:
                    print(f"✅ {check_name.replace('_', ' ').title()} - OK")
                else:
                    print(f"❌ {check_name.replace('_', ' ').title()} - FAILED")
    else:
        print("❌ Base template not found")

def test_no_conflicts():
    """Test that preloader doesn't conflict with existing functionality"""
    print("\n🔍 Testing for Potential Conflicts...")
    
    # Check existing JS files for potential conflicts
    js_files = list((project_dir / 'static' / 'js').glob('*.js'))
    conflict_keywords = ['preloader', 'DOMContentLoaded', 'window.onload']
    
    for js_file in js_files:
        if js_file.name == 'preloader.js':
            continue
            
        try:
            with open(js_file, 'r', encoding='utf-8') as f:
                content = f.read().lower()
                
            has_conflicts = any(keyword.lower() in content for keyword in conflict_keywords)
            if has_conflicts:
                print(f"⚠️  Potential conflict in {js_file.name} - manual review recommended")
            else:
                print(f"✅ No conflicts detected in {js_file.name}")
        except Exception as e:
            print(f"⚠️  Could not analyze {js_file.name}: {e}")

def test_responsiveness():
    """Test that preloader CSS is responsive"""
    print("\n🔍 Testing Responsive Design...")
    
    css_path = project_dir / 'static' / 'css' / 'preloader.css'
    if css_path.exists():
        with open(css_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            responsive_checks = {
                'mobile_media_query': '@media (max-width: 768px)' in content,
                'small_mobile_query': '@media (max-width: 480px)' in content,
                'clamp_function': 'clamp(' in content,
                'viewport_units': 'vw' in content or 'vh' in content
            }
            
            for check_name, result in responsive_checks.items():
                if result:
                    print(f"✅ {check_name.replace('_', ' ').title()} - OK")
                else:
                    print(f"❌ {check_name.replace('_', ' ').title()} - Missing")
    else:
        print("❌ Preloader CSS file not found for responsiveness test")

def test_performance():
    """Test preloader performance characteristics"""
    print("\n🔍 Testing Performance Characteristics...")
    
    js_path = project_dir / 'static' / 'js' / 'preloader.js'
    if js_path.exists():
        with open(js_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
            performance_checks = {
                'minimum_display_time': 'minDisplayTime' in content,
                'maximum_display_time': 'maxDisplayTime' in content,
                'dom_removal': 'removeChild' in content,
                'event_cleanup': 'clearInterval' in content,
                'force_hide_method': 'forceHide' in content
            }
            
            for check_name, result in performance_checks.items():
                if result:
                    print(f"✅ {check_name.replace('_', ' ').title()} - OK")
                else:
                    print(f"❌ {check_name.replace('_', ' ').title()} - Missing")

def main():
    """Run all preloader tests"""
    print("🛡️ Hackversity Cybersecurity Preloader Test Suite")
    print("=" * 50)
    
    try:
        test_static_files()
        test_template_integration()
        test_no_conflicts()
        test_responsiveness()
        test_performance()
        
        print("\n" + "=" * 50)
        print("🎉 Preloader testing completed!")
        print("📋 Summary: Check above for any ❌ items that need attention")
        print("💡 The preloader is designed to enhance UX without affecting existing features")
        
    except Exception as e:
        print(f"\n❌ Test suite error: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())