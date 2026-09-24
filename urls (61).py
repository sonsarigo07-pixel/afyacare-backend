from rest_framework.routers import DefaultRouter; from .views import AppointmentViewSet; r=DefaultRouter(); r.register('', AppointmentViewSet); urlpatterns=r.urls
