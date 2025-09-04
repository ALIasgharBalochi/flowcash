from django.db import models
from users.models import CustomUser 
from datetime import date

class Category(models.Model):
    name = models.CharField(max_length=30)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,blank=True,null=True,related_name='category')
    is_default = models.BooleanField(default=False)

class RecurringExpense(models.Model):
    FREQUENCY_CHOICES = [
        ('daily', 'Daily'),
        ('weekly','Weekly'),
        ('monthly','Monthly'),
        ('yearly', 'Yearly')
    ]

    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='recurring_expenses')
    category = models.ForeignKey(Category,on_delete=models.CASCADE,related_name='recurring_expenses')
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    description = models.CharField(max_length=255,blank=True,null=True)
    frequency = models.CharField(max_length=20,choices=FREQUENCY_CHOICES)
    anchor_date = models.DateField()
    next_run_at = models.DateField(default=date.today())
    active = models.BooleanField(default=True)
    end_date = models.DateField(null=True,blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Expense(models.Model):
    amount = models.DecimalField(max_digits=20,decimal_places=2)
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,blank=True,related_name='expense')
    date = models.DateField()
    description = models.CharField(max_length=255,blank=True,null=True)
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='expense')
    created_at = models.DateTimeField(auto_now_add=True)
    recurring = models.ForeignKey(RecurringExpense,null=True,blank=True,on_delete=models.SET_NULL,related_name='expenses')

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

