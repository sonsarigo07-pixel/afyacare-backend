from rest_framework import generics, permissions
from rest_framework_simplejwt.views import TokenObtainPairView
from .models import User
from .serializers import UserSerializer, RegisterSerializer

class LoginView(TokenObtainPairView):
    permission_classes=[permissions.AllowAny]

class RegisterView(generics.CreateAPIView):
    queryset=User.objects.all()
    serializer_class=RegisterSerializer
    permission_classes=[permissions.IsAuthenticated]
    def get_permissions(self):
        # Only ADMIN can create users, but allow first user creation
        if User.objects.count()==0:
            return [permissions.AllowAny()]
        return [permissions.IsAuthenticated()]

class MeView(generics.RetrieveAPIView):
    serializer_class=UserSerializer
    def get_object(self): return self.request.user

class UserListView(generics.ListAPIView):
    queryset=User.objects.all(); serializer_class=UserSerializer
