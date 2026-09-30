import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'afyacare.settings')
django.setup()

from django.contrib.auth import get_user_model
User = get_user_model()

username = 'admin'
email = 'admin@afyacare.com'
password = 'Afya2024!'

if not User.objects.filter(username=username).exists():
    User.objects.create_superuser(username, email, password)
    print(f"✅ SUPERUSER CREATED: {username} / {password}")
else:
    print(f"User {username} already exists")
