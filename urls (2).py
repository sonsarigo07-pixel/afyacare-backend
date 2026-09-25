
from django.urls import path
from .views import health_check, create_bill_and_push, list_bills, mpesa_callback

urlpatterns = [
    path('health/', health_check),
    path('stk-push/', create_bill_and_push),
    path('bills/', list_bills),
    path('mpesa/callback/', mpesa_callback),
]
