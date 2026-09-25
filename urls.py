from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

def health(request):
    return JsonResponse({"status": "ok", "service": "AfyaCare Backend v10.25", "mpesa": "ready"})

urlpatterns = [
    path('', health),
    path('admin/', admin.site.urls),
    path('api/billing/', include('billing.urls')),
]
