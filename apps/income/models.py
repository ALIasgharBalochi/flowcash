from django.db import models
from django.conf import settings
import uuid
from datetime import datetime

class IncomeCategory(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=7, blank=True, null=True)  # optional
    icon = models.CharField(max_length=50, blank=True, null=True)   # optional
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,null=True,blank=True)
    is_default = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Income(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4, primary_key=True, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    source = models.CharField(max_length=100, blank=True, null=True)
    category = models.ForeignKey(IncomeCategory, on_delete=models.SET_NULL, null=True, blank=True)
    description = models.TextField(blank=True, null=True)
    date = models.DateField(default=datetime.now().date(),blank=True,null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.source or 'Income'} - {self.amount}"

