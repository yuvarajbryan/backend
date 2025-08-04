#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from accounts.models import User

def create_manager_user():
    """Create a manager user for testing"""
    try:
        # Check if manager user already exists
        manager_user = User.objects.filter(username='manager').first()
        if manager_user:
            print(f"Manager user already exists: {manager_user.username}")
            print(f"Password: manager123")
            return
        
        # Create new manager user
        manager_user = User.objects.create_user(
            username='manager',
            email='manager@example.com',
            password='manager123',
            role='manager'
        )
        
        print("✅ Manager user created successfully!")
        print(f"Username: {manager_user.username}")
        print(f"Email: {manager_user.email}")
        print(f"Role: {manager_user.role}")
        print(f"Password: manager123")
        print("\nYou can now login with these credentials!")
        
    except Exception as e:
        print(f"❌ Error creating manager user: {e}")

if __name__ == '__main__':
    create_manager_user() 