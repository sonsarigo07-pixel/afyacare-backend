from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

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
