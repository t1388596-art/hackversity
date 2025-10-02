#!/usr/bin/env python
"""
Production Template Validation Script
Ensures all templates are production-ready with proper static file references
"""
import os
import sys
import django
from pathlib import Path

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

def validate_templates():
    """Validate that all templates are production-ready"""
    from django.template.loader import get_template
    from django.template import TemplateDoesNotExist
    from django.test import RequestFactory
    from django.contrib.auth import get_user_model
    
    print("🔍 Validating templates for production...")
    
    templates_to_check = [
        'base.html',
        'chat/home.html', 
        'accounts/login.html',
        'accounts/signup.html',
        'accounts/profile.html'
    ]
    
    factory = RequestFactory()
    User = get_user_model()
    
    # Create test user for authenticated templates
    try:
        test_user = User.objects.create_user(
            username='template_test_user',
            email='test@example.com',
            password='testpass123'
        )
    except:
        test_user = User.objects.filter(username='template_test_user').first()
    
    for template_name in templates_to_check:
        try:
            print(f"\n📄 Checking template: {template_name}")
            
            # Try to load the template
            template = get_template(template_name)
            print(f"   ✅ Template loads successfully")
            
            # Test template rendering with context
            request = factory.get('/')
            request.user = test_user
            
            if template_name == 'chat/home.html':
                context = {
                    'user': test_user,
                    'conversations': [],
                    'active_conversation': None,
                    'messages': [],
                    'force_chat': False,
                    'request': request
                }
            elif template_name.startswith('accounts/'):
                if 'signup' in template_name:
                    from accounts.forms import CustomUserCreationForm
                    context = {
                        'form': CustomUserCreationForm(),
                        'user': test_user,
                        'request': request
                    }
                else:
                    context = {
                        'user': test_user,
                        'request': request
                    }
            else:
                context = {
                    'user': test_user,
                    'request': request
                }
            
            # Try to render
            try:
                rendered = template.render(context, request)
                print(f"   ✅ Template renders successfully ({len(rendered)} chars)")
                
                # Check for static file references
                if '{% static' in rendered or 'static/' in rendered:
                    print(f"   ✅ Contains static file references")
                else:
                    print(f"   ⚠️  No static file references found")
                    
                # Check for responsive design
                if 'viewport' in rendered and 'device-width' in rendered:
                    print(f"   ✅ Responsive viewport meta tag present")
                else:
                    print(f"   ⚠️  No responsive viewport meta tag")
                    
            except Exception as render_error:
                print(f"   ❌ Template rendering error: {render_error}")
                
        except TemplateDoesNotExist:
            print(f"   ❌ Template not found: {template_name}")
        except Exception as e:
            print(f"   ❌ Template error: {e}")
    
    # Clean up test user
    try:
        User.objects.filter(username='template_test_user').delete()
    except:
        pass
    
    print(f"\n🔍 Checking static files...")
    
    # Check critical static files
    static_files = [
        'css/style.css',
        'js/chat.js'
    ]
    
    for static_file in static_files:
        static_path = Path('static') / static_file
        if static_path.exists():
            print(f"   ✅ {static_file} exists ({static_path.stat().st_size} bytes)")
        else:
            print(f"   ❌ {static_file} missing")
    
    # Check staticfiles directory (production)
    staticfiles_dir = Path('staticfiles')
    if staticfiles_dir.exists():
        print(f"   ✅ staticfiles directory exists")
        collected_files = list(staticfiles_dir.rglob('*'))
        print(f"   ✅ {len(collected_files)} files collected for production")
    else:
        print(f"   ⚠️  staticfiles directory not found - run collectstatic")
    
    print(f"\n🎉 Template validation completed!")

def check_production_settings():
    """Check Django settings for production readiness"""
    from django.conf import settings
    
    print(f"\n⚙️  Checking production settings...")
    
    # Static files configuration
    print(f"   STATIC_URL: {settings.STATIC_URL}")
    print(f"   STATIC_ROOT: {settings.STATIC_ROOT}")
    print(f"   STATICFILES_DIRS: {settings.STATICFILES_DIRS}")
    
    # Template configuration
    for template_engine in settings.TEMPLATES:
        if template_engine['BACKEND'] == 'django.template.backends.django.DjangoTemplates':
            print(f"   Template DIRS: {template_engine['DIRS']}")
            print(f"   Template APP_DIRS: {template_engine['APP_DIRS']}")
    
    # WhiteNoise for static files
    if 'whitenoise.middleware.WhiteNoiseMiddleware' in settings.MIDDLEWARE:
        print(f"   ✅ WhiteNoise middleware configured")
    else:
        print(f"   ⚠️  WhiteNoise middleware not found")
    
    print(f"   STATICFILES_STORAGE: {getattr(settings, 'STATICFILES_STORAGE', 'Default')}")

if __name__ == '__main__':
    try:
        validate_templates()
        check_production_settings()
        print(f"\n✨ All checks completed successfully!")
    except Exception as e:
        print(f"\n❌ Error during validation: {e}")
        sys.exit(1)