from rest_framework.routers import DefaultRouter; from .views import PatientViewSet; r=DefaultRouter(); r.register('', PatientViewSet); urlpatterns=r.urls
