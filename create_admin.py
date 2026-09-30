import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afyacare.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

# Delete old admin if exists
User.objects.filter(username='admin').delete()
print("Old admin deleted")

# Create fresh
User.objects.create_superuser('admin', 'admin@afyacare.com', 'Afya2024!')
print("✅ NEW ADMIN CREATED: admin / Afya2024!")
