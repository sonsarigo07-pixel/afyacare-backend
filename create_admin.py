import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afyacare.settings')
django.setup()
from django.contrib.auth import get_user_model
User = get_user_model()
User.objects.filter(username='admin').delete()
User.objects.create_superuser('admin', 'admin@afyacare.com', 'Afya2024!')
print("✅ ADMIN READY: admin / Afya2024!")
