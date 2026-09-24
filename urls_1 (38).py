from rest_framework.routers import DefaultRouter; from .views import DrugViewSet; r=DefaultRouter(); r.register('drugs', DrugViewSet); urlpatterns=r.urls
