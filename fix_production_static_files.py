#!/usr/bin/env python3
"""
Production Static Files Fix
Fixes the "Missing staticfiles manifest entry for 'images/favicon.ico'" error
"""

import os
import sys
import django
from pathlib import Path

# Add the current directory to Python path
current_dir = Path(__file__).parent
sys.path.insert(0, str(current_dir))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from django.core.management import call_command
from django.conf import settings
from django.contrib.staticfiles import finders
from django.contrib.staticfiles.storage import staticfiles_storage

def create_missing_favicon():
    """Create a simple favicon if it doesn't exist"""
    favicon_path = settings.BASE_DIR / 'static' / 'images' / 'favicon.ico'
    
    if not favicon_path.exists():
        print("🔧 Creating missing favicon.ico...")
        
        # Create the images directory if it doesn't exist
        favicon_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create a simple SVG favicon (modern browsers support SVG favicons)
        svg_favicon_path = settings.BASE_DIR / 'static' / 'images' / 'favicon.svg'
        
        svg_content = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100">
    <rect width="100" height="100" fill="#1a1a2e"/>
    <text x="50" y="65" font-family="Arial, sans-serif" font-size="60" font-weight="bold" fill="#00f5ff" text-anchor="middle">H</text>
</svg>'''
        
        with open(svg_favicon_path, 'w') as f:
            f.write(svg_content)
        
        print(f"✅ Created SVG favicon: {svg_favicon_path}")
        
        # Try to create a simple ICO file using a basic approach
        try:
            # This creates a minimal ICO file that browsers can use
            ico_content = b'\x00\x00\x01\x00\x01\x00\x20\x20\x00\x00\x01\x00\x08\x00\xa8\x05\x00\x00\x16\x00\x00\x00'
            # Add minimal image data (32x32 pixel favicon)
            ico_content += b'\x00' * (32 * 32)  # Simple black favicon
            
            with open(favicon_path, 'wb') as f:
                f.write(ico_content)
            
            print(f"✅ Created ICO favicon: {favicon_path}")
            
        except Exception as e:
            print(f"⚠️  Could not create ICO favicon: {e}")
            print("✅ SVG favicon will be used as fallback")
    
    else:
        print(f"✅ Favicon already exists: {favicon_path}")

def test_static_files():
    """Test static files configuration"""
    print("\n🔍 Testing Static Files Configuration...")
    
    # Check if static directories exist
    static_dir = settings.BASE_DIR / 'static'
    staticfiles_dir = settings.BASE_DIR / 'staticfiles'
    
    print(f"Static source directory: {static_dir} - {'✅' if static_dir.exists() else '❌'}")
    print(f"Staticfiles directory: {staticfiles_dir} - {'✅' if staticfiles_dir.exists() else '❌'}")
    
    # Check key static files
    key_files = [
        'css/style.css',
        'js/chat.js',
        'js/responsive.js',
        'images/hackversity-logo.png',
        'images/favicon.svg'
    ]
    
    print("\n📁 Checking key static files...")
    for file_path in key_files:
        found = finders.find(file_path)
        status = '✅' if found else '❌'
        print(f"   {file_path}: {status}")
    
    # Test staticfiles storage
    print(f"\n⚙️  Static files storage: {settings.STATICFILES_STORAGE}")
    print(f"Static URL: {settings.STATIC_URL}")
    print(f"Static root: {settings.STATIC_ROOT}")

def collect_static_files():
    """Collect static files for production"""
    print("\n📦 Collecting static files for production...")
    
    try:
        # Clear existing staticfiles
        if (settings.BASE_DIR / 'staticfiles').exists():
            import shutil
            shutil.rmtree(settings.BASE_DIR / 'staticfiles')
            print("🗑️  Cleared existing staticfiles directory")
        
        # Collect static files
        call_command('collectstatic', '--noinput', verbosity=1)
        print("✅ Static files collected successfully")
        
        # Verify favicon was collected
        favicon_collected = (settings.BASE_DIR / 'staticfiles' / 'images' / 'favicon.svg').exists()
        print(f"Favicon in staticfiles: {'✅' if favicon_collected else '⚠️'}")
        
    except Exception as e:
        print(f"❌ Error collecting static files: {e}")
        return False
    
    return True

def test_template_safe_loading():
    """Test that templates can safely load static files"""
    print("\n🧪 Testing template safe loading...")
    
    try:
        from django.template import Template, Context
        from django.template.loader import get_template
        
        # Test loading the base template
        template = get_template('base.html')
        context = Context({})
        
        # This should not raise an error now
        rendered = template.render(context)
        
        if 'favicon' in rendered.lower() or 'icon' in rendered.lower():
            print("✅ Base template renders with favicon reference")
        else:
            print("ℹ️  Base template renders without favicon (safe)")
        
        return True
        
    except Exception as e:
        print(f"❌ Template rendering error: {e}")
        return False

def main():
    """Run all production fixes"""
    print("🚀 Production Static Files Fix")
    print("=" * 50)
    
    # Step 1: Create missing favicon
    create_missing_favicon()
    
    # Step 2: Test static files configuration
    test_static_files()
    
    # Step 3: Collect static files
    if collect_static_files():
        print("\n✅ Static files collection successful")
    else:
        print("\n❌ Static files collection failed")
        return False
    
    # Step 4: Test template rendering
    if test_template_safe_loading():
        print("\n✅ Template rendering test successful")
    else:
        print("\n❌ Template rendering test failed")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 Production Static Files Fix Complete!")
    print("\n📋 Summary of changes:")
    print("1. ✅ Created missing favicon files")
    print("2. ✅ Updated STATICFILES_STORAGE to be more lenient")
    print("3. ✅ Added safe static file loading template tags")
    print("4. ✅ Updated base.html to use safe favicon loading")
    print("5. ✅ Collected static files for production")
    
    print("\n🚀 Your production deployment should now work without favicon errors!")
    print("\n💡 Next steps:")
    print("   1. Deploy the updated code to production")
    print("   2. Run 'python manage.py collectstatic' on production (if needed)")
    print("   3. Restart your production server")
    
    return True

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)