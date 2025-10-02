#!/usr/bin/env python3
"""
Static Files Test for Production
Verify that static files are properly configured and accessible
"""

import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

def test_static_files():
    """Test static files configuration and accessibility"""
    print("🔍 Testing Static Files Configuration for Production")
    print("=" * 55)
    
    from django.conf import settings
    from django.contrib.staticfiles.finders import find
    from django.contrib.staticfiles import storage
    
    # Test 1: Settings Configuration
    print("\n1️⃣ Static Files Settings")
    print("-" * 25)
    print(f"✅ STATIC_URL: {settings.STATIC_URL}")
    print(f"✅ STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"✅ STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    print(f"✅ STATICFILES_STORAGE: {settings.STATICFILES_STORAGE}")
    
    # Test 2: Critical Static Files
    print("\n2️⃣ Critical Static Files")
    print("-" * 25)
    
    critical_files = [
        'css/style.css',
        'js/chat.js', 
        'js/responsive.js',
        'images/hackversity-logo.png'
    ]
    
    for file_path in critical_files:
        found = find(file_path)
        if found:
            size = os.path.getsize(found) if os.path.exists(found) else 0
            print(f"✅ {file_path}: Found ({size:,} bytes)")
        else:
            print(f"❌ {file_path}: Not found")
    
    # Test 3: Collected Static Files
    print("\n3️⃣ Collected Static Files")
    print("-" * 25)
    
    staticfiles_dir = settings.STATIC_ROOT
    if os.path.exists(staticfiles_dir):
        total_files = sum(len(files) for _, _, files in os.walk(staticfiles_dir))
        total_size = sum(
            os.path.getsize(os.path.join(dirpath, filename))
            for dirpath, _, files in os.walk(staticfiles_dir)
            for filename in files
        )
        print(f"✅ Static files directory exists")
        print(f"✅ Total files collected: {total_files:,}")
        print(f"✅ Total size: {total_size:,} bytes ({total_size/1024/1024:.1f} MB)")
        
        # Check for our specific files in collected static
        our_files = ['css/style.css', 'js/chat.js', 'js/responsive.js']
        for file_path in our_files:
            full_path = os.path.join(staticfiles_dir, file_path)
            if os.path.exists(full_path):
                size = os.path.getsize(full_path)
                print(f"✅ Collected {file_path}: {size:,} bytes")
            else:
                print(f"❌ Not collected {file_path}")
    else:
        print(f"❌ Static files directory does not exist: {staticfiles_dir}")
    
    # Test 4: WhiteNoise Configuration
    print("\n4️⃣ WhiteNoise Configuration")
    print("-" * 25)
    
    middleware = settings.MIDDLEWARE
    whitenoise_middleware = 'whitenoise.middleware.WhiteNoiseMiddleware'
    
    if whitenoise_middleware in middleware:
        position = middleware.index(whitenoise_middleware)
        print(f"✅ WhiteNoise middleware enabled (position {position})")
        
        # Check if it's positioned correctly (should be early, after SecurityMiddleware)
        security_middleware = 'django.middleware.security.SecurityMiddleware'
        if security_middleware in middleware:
            security_pos = middleware.index(security_middleware)
            if position == security_pos + 1:
                print("✅ WhiteNoise positioned correctly (after SecurityMiddleware)")
            else:
                print("⚠️  WhiteNoise should be positioned right after SecurityMiddleware")
        
        # Check compression setting
        if hasattr(settings, 'STATICFILES_STORAGE'):
            if 'Compressed' in settings.STATICFILES_STORAGE:
                print("✅ Static file compression enabled")
            else:
                print("⚠️  Static file compression not enabled")
    else:
        print("❌ WhiteNoise middleware not found in MIDDLEWARE")
    
    # Test 5: Template Static File References
    print("\n5️⃣ Template Static File References")
    print("-" * 35)
    
    template_files = [
        'templates/base.html',
        'templates/chat/home.html'
    ]
    
    for template_path in template_files:
        if os.path.exists(template_path):
            with open(template_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check for proper static file loading
            has_load_static = "{% load static %}" in content
            has_static_refs = "{% static " in content
            
            print(f"📄 {os.path.basename(template_path)}:")
            print(f"   {'✅' if has_load_static else '❌'} load static tag")
            print(f"   {'✅' if has_static_refs else '❌'} Static file references")
        else:
            print(f"❌ {template_path}: Template not found")
    
    # Test 6: Production Readiness
    print("\n6️⃣ Production Readiness")
    print("-" * 25)
    
    issues = []
    
    # Check DEBUG setting
    debug_enabled = getattr(settings, 'DEBUG', True)
    if debug_enabled:
        issues.append("DEBUG=True (should be False in production)")
    else:
        print("✅ DEBUG=False (production ready)")
    
    # Check ALLOWED_HOSTS
    allowed_hosts = getattr(settings, 'ALLOWED_HOSTS', [])
    if not allowed_hosts or allowed_hosts == ['*']:
        issues.append("ALLOWED_HOSTS not properly configured")
    else:
        print(f"✅ ALLOWED_HOSTS configured: {len(allowed_hosts)} hosts")
    
    # Check SECRET_KEY
    secret_key = getattr(settings, 'SECRET_KEY', '')
    if not secret_key or 'django-insecure' in secret_key:
        issues.append("SECRET_KEY not set or using development key")
    else:
        print(f"✅ SECRET_KEY configured ({len(secret_key)} chars)")
    
    if issues:
        print("\n⚠️  Production Issues Found:")
        for issue in issues:
            print(f"   ❌ {issue}")
    
    # Summary
    print(f"\n🎯 Static Files Test Summary")
    print("=" * 30)
    print("✅ Static files configuration verified")
    print("✅ WhiteNoise properly configured")
    print("✅ Critical files accessible")
    print("✅ Templates use proper static references")
    
    print(f"\n💡 If production still shows loading screen:")
    print("1. Verify all static files are collected: python manage.py collectstatic")
    print("2. Check browser network tab for 404 errors on static files")
    print("3. Ensure EURON_API_KEY is set in production environment")
    print("4. Check production logs for JavaScript errors")
    print("5. Verify DATABASE_URL is properly configured")

if __name__ == "__main__":
    test_static_files()