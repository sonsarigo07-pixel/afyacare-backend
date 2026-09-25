
from django.db import models
class Patient(models.Model):
    name=models.CharField(max_length=100)
    phone=models.CharField(max_length=20)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
class Bill(models.Model):
    patient=models.ForeignKey(Patient,on_delete=models.CASCADE)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    description=models.CharField(max_length=200, default='Consultation')
    is_paid=models.BooleanField(default=False)
    created_at=models.DateTimeField(auto_now_add=True)
class Payment(models.Model):
    bill=models.ForeignKey(Bill,on_delete=models.CASCADE)
    mpesa_receipt=models.CharField(max_length=50, blank=True)
    amount=models.DecimalField(max_digits=10,decimal_places=2)
    phone=models.CharField(max_length=20)
    status=models.CharField(max_length=20, default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
