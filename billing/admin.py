
from django.contrib import admin
from .models import Patient, Bill, Payment
admin.site.register(Patient); admin.site.register(Bill); admin.site.register(Payment)
