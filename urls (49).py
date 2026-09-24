from django.urls import path
from .views import LoginView, RegisterView, MeView, UserListView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns=[
    path('login/', LoginView.as_view(), name='login'),
    path('refresh/', TokenRefreshView.as_view()),
    path('register/', RegisterView.as_view()),
    path('me/', MeView.as_view()),
    path('users/', UserListView.as_view()),
]
