from django.contrib import admin
from django.urls import path
from django.http import JsonResponse

def home(request):
    return JsonResponse({
        "status": "AfyaCare Backend is LIVE 🎉",
        "message": "Welcome to AfyaCare API",
        "admin": "/admin/",
        "api": "/api/ - coming soon",
        "version": "v10.25"
    })

urlpatterns = [
    path('', home, name='home'),
    path('admin/', admin.site.urls),
]
