from django.contrib.auth import get_user_model
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecom_inventory.settings')
django.setup()

User = get_user_model()
admin = User.objects.get(username='admin')
admin.set_password('admin123')
admin.is_staff = True
admin.is_superuser = True
admin.save()
print("Admin password set to: admin123")
