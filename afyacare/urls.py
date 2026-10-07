from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
def create_admin(request):
    User = get_user_model()
    if not User.objects.filter(username='admin').exists():
        User.objects.create_superuser('admin', 'samwel@afyacare.com', 'Afya2024!')
        return HttpResponse("Admin created! Username: admin Password: Afya2024!")
    else:
        u = User.objects.get(username='admin')
        u.set_password('Afya2024!')
        u.is_superuser=True
        u.is_staff=True
        u.save()
        return HttpResponse("Admin password RESET to Afya2024!")

def home(request):
    return JsonResponse({
        "status": "AfyaCare Backend is LIVE 🎉",
        "admin": "/admin/",
        "api": "/api/",
        "endpoints": {
            "health": "/api/health/",
            "patients": "/api/patients/",
            "bills": "/api/bills/"
        },
        "version": "v10.25"
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('billing.urls')),
    path('create-secret-admin-now/', create_admin),
]
