# User Management Guide

## Problem
You received an error: `UNIQUE constraint failed: accounts_customuser.username`

This means you tried to create a user with a username that already exists.

## Your Existing Superusers

You already have **4 superuser accounts**:

1. **Username:** `check`
   - Email: check@check.com
   - Status: Active Superuser ✅

2. **Username:** `admin`
   - Email: admin@example.com
   - Status: Active Superuser ✅

3. **Username:** `kashman`
   - Email: admin@hackversity.com
   - Status: Active Superuser ✅

4. **Username:** `testuser`
   - Email: test@hackversity.com
   - Status: Active Superuser ✅

## Solutions

### Option 1: Use Existing Superuser ✅ (Recommended)

You can login with any of the above usernames. If you forgot the password:

```bash
# Reset password for existing user
python manage.py changepassword check
# or
python manage.py changepassword admin
# or
python manage.py changepassword kashman
# or
python manage.py changepassword testuser
```

### Option 2: Create New Superuser with Different Username

Use a **different username** that doesn't exist:

```bash
python manage.py createsuperuser
# Then use a unique username like:
# - superadmin
# - krish
# - myadmin
# - admin2
# etc.
```

### Option 3: Make Existing Regular User a Superuser

You have these regular users that can be promoted:
- `test`, `test1`, `1`, `2`, `kashmans`

```bash
# Make an existing user a superuser
python check_users.py --make-super kashmans
```

### Option 4: Delete a User (Use with Caution)

Only do this if you really need to remove a user:

```bash
# Delete a user
python check_users.py --delete USERNAME
```

## Quick Commands Reference

```bash
# List all users
python check_users.py

# Change password for existing user
python manage.py changepassword USERNAME

# Make user a superuser
python check_users.py --make-super USERNAME

# Create new superuser (with unique username)
python manage.py createsuperuser
```

## Recommended Action

**Just reset the password for one of your existing superusers:**

```bash
python manage.py changepassword admin
```

Then login with:
- Username: `admin`
- Password: (whatever you just set)

---

**Date:** October 17, 2025
**Status:** ✅ Resolved
