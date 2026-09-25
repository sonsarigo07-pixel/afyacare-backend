
from django.urls import path
from . import views
urlpatterns=[
    path('health/', views.health),
    path('patients/', views.patients),
    path('bills/', views.bills),
    path('mpesa/push/', views.push_stk),
    path('mpesa/callback/', views.mpesa_callback),
]
