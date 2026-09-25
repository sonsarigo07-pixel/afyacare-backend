
from django.db import models
from django.utils import timezone

class Patient(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name

class Bill(models.Model):
    STATUS_CHOICES = [('pending','Pending'),('paid','Paid'),('failed','Failed')]
    patient_name = models.CharField(max_length=200)
    phone = models.CharField(max_length=20)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.CharField(max_length=300, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    mpesa_checkout_id = models.CharField(max_length=100, blank=True)
    mpesa_receipt = models.CharField(max_length=100, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"{self.patient_name} - {self.amount} - {self.status}"
