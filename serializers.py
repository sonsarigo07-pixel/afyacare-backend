
from rest_framework import serializers
from .models import Bill, Patient
class BillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = '__all__'
