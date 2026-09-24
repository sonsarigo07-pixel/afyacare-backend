from rest_framework import serializers
from .models import Invoice, InvoiceItem, MpesaTransaction

class InvoiceItemSerializer(serializers.ModelSerializer):
    class Meta: model=InvoiceItem; fields='__all__'

class InvoiceSerializer(serializers.ModelSerializer):
    items=InvoiceItemSerializer(many=True, required=False)
    class Meta: model=Invoice; fields='__all__'
    def create(self, validated):
        items_data=validated.pop('items', [])
        inv=Invoice.objects.create(**validated)
        for item in items_data:
            InvoiceItem.objects.create(invoice=inv, **item)
        return inv

class MpesaTransactionSerializer(serializers.ModelSerializer):
    class Meta: model=MpesaTransaction; fields='__all__'
