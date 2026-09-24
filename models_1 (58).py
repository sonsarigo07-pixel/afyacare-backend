from django.db import models
from patients.models import Patient
from django.conf import settings

class Appointment(models.Model):
    STATUS=[('SCHEDULED','Scheduled'),('WAITING','Waiting'),('IN_PROGRESS','With Doctor'),('COMPLETED','Completed'),('CANCELLED','Cancelled'),('NO_SHOW','No Show')]
    patient=models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments')
    doctor=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='doctor_appointments')
    date=models.DateField(); time=models.TimeField()
    reason=models.TextField()
    status=models.CharField(max_length=20, choices=STATUS, default='SCHEDULED')
    created_by=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_appointments')
    created_at=models.DateTimeField(auto_now_add=True)

    def __str__(self): return f"{self.patient} - {self.date} {self.time}"
