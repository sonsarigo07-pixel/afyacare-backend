from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import InvoiceViewSet, MpesaViewSet, initiate_stk_push, mpesa_callback

r=DefaultRouter()
r.register('invoices', InvoiceViewSet)
r.register('mpesa-transactions', MpesaViewSet)

urlpatterns = r.urls + [
    path('mpesa/stk-push/', initiate_stk_push, name='mpesa-stk'),
    path('mpesa/callback/', mpesa_callback, name='mpesa-callback'),
]
