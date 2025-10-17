#!/usr/bin/env python
"""
Test Learning Module Functionality
This script creates sample learning modules to test the admin interface.
"""

import os
import sys
import django
from pathlib import Path

# Add the project directory to Python path
project_dir = Path(__file__).resolve().parent
sys.path.append(str(project_dir))

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'genai_project.settings')
django.setup()

from chat.models import LearningModule, LearningVideo

def create_sample_modules():
    """Create sample learning modules for testing"""
    print("🚀 Creating sample learning modules...")
    
    # Create first module: Getting Started
    module1, created = LearningModule.objects.get_or_create(
        slug='getting-started',
        defaults={
            'title': 'Getting Started with Cybersecurity',
            'description': 'Learn the fundamentals of cybersecurity and ethical hacking from scratch.',
            'icon': 'fas fa-seedling',
            'order': 1,
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Created module: {module1.title}")
        
        # Add sample videos to the module
        video1 = LearningVideo.objects.create(
            module=module1,
            title='Introduction to Cybersecurity',
            youtube_id='ePD7cLWkt-E',  # Sample YouTube ID
            duration_minutes=15,
            order=1,
            is_active=True
        )
        
        video2 = LearningVideo.objects.create(
            module=module1,
            title='Basic Security Concepts',
            youtube_id='dQw4w9WgXcQ',  # Sample YouTube ID
            duration_minutes=20,
            order=2,
            is_active=True
        )
        
        print(f"  📹 Added video: {video1.title}")
        print(f"  📹 Added video: {video2.title}")
    else:
        print(f"⚠️  Module already exists: {module1.title}")
    
    # Create second module: Network Security
    module2, created = LearningModule.objects.get_or_create(
        slug='network-security',
        defaults={
            'title': 'Network Security Fundamentals',
            'description': 'Master network protocols, scanning techniques, and penetration testing.',
            'icon': 'fas fa-network-wired',
            'order': 2,
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Created module: {module2.title}")
        
        # Add sample videos
        video3 = LearningVideo.objects.create(
            module=module2,
            title='Network Scanning Basics',
            youtube_id='oHg5SJYRHA0',  # Sample YouTube ID
            duration_minutes=25,
            order=1,
            is_active=True
        )
        
        print(f"  📹 Added video: {video3.title}")
    else:
        print(f"⚠️  Module already exists: {module2.title}")
    
    # Create third module: Web Security
    module3, created = LearningModule.objects.get_or_create(
        slug='web-security',
        defaults={
            'title': 'Web Application Security',
            'description': 'Discover web vulnerabilities like XSS, SQL injection, and secure coding practices.',
            'icon': 'fas fa-globe',
            'order': 3,
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Created module: {module3.title}")
    else:
        print(f"⚠️  Module already exists: {module3.title}")
    
    print("\n📊 Current Learning Modules:")
    modules = LearningModule.objects.filter(is_active=True).order_by('order')
    for module in modules:
        video_count = module.videos.filter(is_active=True).count()
        print(f"  • {module.title} ({video_count} videos) - Slug: {module.slug}")
    
    print(f"\n🎉 Total active modules: {modules.count()}")
    print("\n📝 Next steps:")
    print("1. Run: python manage.py runserver")
    print("2. Visit: http://127.0.0.1:8000/chat/learning/")
    print("3. Login to admin: http://127.0.0.1:8000/admin/")
    print("4. Add more modules in admin panel!")

def main():
    """Main function"""
    print("🧪 Testing Learning Module Functionality")
    print("=" * 50)
    
    try:
        create_sample_modules()
        print("\n✅ Learning module test completed successfully!")
        return True
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    main()