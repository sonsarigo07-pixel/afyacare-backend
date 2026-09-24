from django.db import models
from patients.models import Patient
from appointments.models import Appointment
from django.conf import settings

class Consultation(models.Model):
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE)
    appointment=models.ForeignKey(Appointment, on_delete=models.SET_NULL, null=True, blank=True)
    doctor=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    chief_complaint=models.TextField()
    history=models.TextField(blank=True)
    examination=models.TextField(blank=True)
    diagnosis=models.TextField()
    treatment_plan=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True)

class Prescription(models.Model):
    consultation=models.ForeignKey(Consultation, on_delete=models.CASCADE, related_name='prescriptions')
    drug_name=models.CharField(max_length=200); dosage=models.CharField(max_length=100)
    frequency=models.CharField(max_length=100); duration=models.CharField(max_length=100)
    notes=models.TextField(blank=True)
