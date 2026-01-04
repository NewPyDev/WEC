#!/usr/bin/env python
"""
Script to set default company names for existing users
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_inventory.settings')
django.setup()

from accounts.models import User

def set_default_company_names():
    """Set default company name for users who don't have one"""
    users_updated = 0
    
    for user in User.objects.all():
        if not user.shipping_company_name:
            user.shipping_company_name = 'ECOMMERCE INVENTORY'
            user.save()
            users_updated += 1
            print(f"Updated {user.username} with default company name")
    
    print(f"\n✅ Updated {users_updated} users with default company name")
    print("All users can now customize their company name in Profile → Shipping Company Name")

if __name__ == '__main__':
    set_default_company_names()
