from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User; fields=['id','username','email','first_name','last_name','role','phone']

class RegisterSerializer(serializers.ModelSerializer):
    password=serializers.CharField(write_only=True)
    class Meta:
        model=User; fields=['username','password','email','first_name','last_name','role','phone']
    def create(self, validated):
        user=User.objects.create_user(**validated)
        return user
