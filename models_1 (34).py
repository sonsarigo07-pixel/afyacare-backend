from django.db import models
class Drug(models.Model):
    name=models.CharField(max_length=200); category=models.CharField(max_length=100, blank=True)
    stock=models.IntegerField(default=0); min_stock=models.IntegerField(default=10)
    unit_price=models.DecimalField(max_digits=10, decimal_places=2)
    expiry_date=models.DateField(null=True, blank=True)
    supplier=models.CharField(max_length=200, blank=True)
    created_at=models.DateTimeField(auto_now_add=True)
    def __str__(self): return self.name
    @property
    def is_low_stock(self): return self.stock <= self.min_stock
