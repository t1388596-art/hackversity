#!/usr/bin/env python
"""
Check and manage existing users
This script helps identify existing users and provides options to manage them.
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

from django.contrib.auth import get_user_model

User = get_user_model()

def check_users():
    """Check all existing users in the database"""
    print("👥 Checking Existing Users")
    print("=" * 60)
    
    users = User.objects.all()
    
    if not users.exists():
        print("\n✅ No users found in the database.")
        print("   You can safely create a superuser now.")
        return
    
    print(f"\n📊 Found {users.count()} user(s) in the database:\n")
    
    for user in users:
        print(f"  Username: {user.username}")
        print(f"  Email: {user.email}")
        print(f"  Is Superuser: {'Yes' if user.is_superuser else 'No'}")
        print(f"  Is Staff: {'Yes' if user.is_staff else 'No'}")
        print(f"  Is Active: {'Yes' if user.is_active else 'No'}")
        print(f"  Date Joined: {user.date_joined}")
        print("-" * 60)
    
    print("\n💡 Solutions:")
    print("\n1. Use a different username when creating superuser")
    print("   Example: admin2, superadmin, myusername, etc.")
    
    print("\n2. Delete an existing user (if needed):")
    print("   Run: python manage.py shell")
    print("   >>> from django.contrib.auth import get_user_model")
    print("   >>> User = get_user_model()")
    print("   >>> User.objects.get(username='USERNAME_HERE').delete()")
    
    print("\n3. Reset password for existing user:")
    print("   Run: python manage.py changepassword USERNAME")
    
    print("\n4. Make existing user a superuser:")
    print("   Run this script with --make-super USERNAME")
    

def make_superuser(username):
    """Make an existing user a superuser"""
    try:
        user = User.objects.get(username=username)
        user.is_superuser = True
        user.is_staff = True
        user.save()
        print(f"✅ User '{username}' is now a superuser!")
        print(f"   Email: {user.email}")
        print(f"   You can login to admin with this user.")
    except User.DoesNotExist:
        print(f"❌ User '{username}' does not exist.")
        print(f"   Available users:")
        for u in User.objects.all():
            print(f"   - {u.username}")


def delete_user(username):
    """Delete a user"""
    try:
        user = User.objects.get(username=username)
        user.delete()
        print(f"✅ User '{username}' has been deleted.")
    except User.DoesNotExist:
        print(f"❌ User '{username}' does not exist.")


def main():
    """Main function"""
    if len(sys.argv) > 1:
        if sys.argv[1] == '--make-super' and len(sys.argv) > 2:
            make_superuser(sys.argv[2])
        elif sys.argv[1] == '--delete' and len(sys.argv) > 2:
            confirm = input(f"Are you sure you want to delete user '{sys.argv[2]}'? (yes/no): ")
            if confirm.lower() == 'yes':
                delete_user(sys.argv[2])
            else:
                print("❌ Deletion cancelled.")
        else:
            print("Usage:")
            print("  python check_users.py                    # List all users")
            print("  python check_users.py --make-super USER  # Make user a superuser")
            print("  python check_users.py --delete USER      # Delete a user")
    else:
        check_users()


if __name__ == '__main__':
    main()
