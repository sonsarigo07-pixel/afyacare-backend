from rest_framework import serializers; from .models import Drug; class DrugSerializer(serializers.ModelSerializer):
    is_low_stock=serializers.ReadOnlyField()
    class Meta: model=Drug; fields='__all__'
