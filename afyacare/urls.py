from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "AfyaCare Backend is LIVE 🎉",
        "message": "Welcome to AfyaCare API",
        "admin": "/admin/",
        "api": "/api/",
        "endpoints": {
            "health": "/api/health/",
            "patients": "/api/patients/",
            "bills": "/api/bills/",
            "mpesa_push": "/api/mpesa/push/",
            "mpesa_callback": "/api/mpesa/callback/"
        },
        "version": "v10.25"
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
    path('api/', include('billing.urls')),
]
