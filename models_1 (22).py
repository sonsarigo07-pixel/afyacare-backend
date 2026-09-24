from django.db import models

class Patient(models.Model):
    GENDER=[('M','Male'),('F','Female'),('O','Other')]
    patient_no=models.CharField(max_length=20, unique=True)
    first_name=models.CharField(max_length=100); last_name=models.CharField(max_length=100)
    id_number=models.CharField(max_length=20, blank=True); sha_number=models.CharField(max_length=30, blank=True)
    phone=models.CharField(max_length=20); email=models.EmailField(blank=True)
    dob=models.DateField(); gender=models.CharField(max_length=1, choices=GENDER)
    address=models.TextField(blank=True)
    next_of_kin_name=models.CharField(max_length=100, blank=True); next_of_kin_phone=models.CharField(max_length=20, blank=True)
    blood_group=models.CharField(max_length=5, blank=True); allergies=models.TextField(blank=True)
    created_at=models.DateTimeField(auto_now_add=True); updated_at=models.DateTimeField(auto_now=True)

    def __str__(self): return f"{self.patient_no} - {self.first_name} {self.last_name}"
    @property
    def full_name(self): return f"{self.first_name} {self.last_name}"
