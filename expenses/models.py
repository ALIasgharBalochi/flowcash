from django.db import models
from users.models import CustomUser 

class Category(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True,related_name='category')
    is_default = models.BooleanField(default=False)

class Expense(models.Model):
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='expense')
    date = models.DateField()
    description = models.CharField(max_length=255,blank=True,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='expense')
    created_at = models.DateTimeField(auto_now_add=True)

class Budget(models.Model):
    PERIOD_CHOICES = [
        ("monthly","Monthly"),
        ("weekly",'Weekly'),
        ("yearly","Yearly")
    ]
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='budgets')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='budgets')
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    period = models.CharField(max_length=20,choices=PERIOD_CHOICES,default="monthly")
    created_at = models.DateTimeField(auto_now_add=True)

