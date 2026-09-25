
from rest_framework import serializers
from .models import Patient,Bill,Payment
class PatientSerializer(serializers.ModelSerializer):
    class Meta: model=Patient; fields='__all__'
class BillSerializer(serializers.ModelSerializer):
    class Meta: model=Bill; fields='__all__'
class PaymentSerializer(serializers.ModelSerializer):
    class Meta: model=Payment; fields='__all__'
