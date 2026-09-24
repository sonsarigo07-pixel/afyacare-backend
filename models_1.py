from django.db import models
from patients.models import Patient
from django.conf import settings

class Invoice(models.Model):
    PAYMENT_METHOD=[('CASH','Cash'),('MPESA','M-Pesa'),('SHA','SHA Insurance'),('BANK','Bank')]
    STATUS=[('PENDING','Pending'),('PAID','Paid'),('PARTIAL','Partial'),('CANCELLED','Cancelled')]
    invoice_no=models.CharField(max_length=20, unique=True)
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    total_amount=models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid=models.DecimalField(max_digits=10, decimal_places=2, default=0)
    payment_method=models.CharField(max_length=20, choices=PAYMENT_METHOD, default='CASH')
    status=models.CharField(max_length=20, choices=STATUS, default='PENDING')
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created_at=models.DateTimeField(auto_now_add=True)

class InvoiceItem(models.Model):
    invoice=models.ForeignKey(Invoice, on_delete=models.CASCADE, related_name='items')
    description=models.CharField(max_length=200)
    quantity=models.IntegerField(default=1)
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)
    amount=models.DecimalField(max_digits=10, decimal_places=2)

class MpesaTransaction(models.Model):
    STATUS=[('PENDING','Pending'),('COMPLETED','Completed'),('FAILED','Failed')]
    invoice=models.ForeignKey(Invoice, on_delete=models.CASCADE, null=True, blank=True)
    phone_number=models.CharField(max_length=20)
    amount=models.DecimalField(max_digits=10, decimal_places=2)
    checkout_request_id=models.CharField(max_length=100, blank=True)
    merchant_request_id=models.CharField(max_length=100, blank=True)
    mpesa_receipt=models.CharField(max_length=100, blank=True)
    status=models.CharField(max_length=20, choices=STATUS, default='PENDING')
    result_desc=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
