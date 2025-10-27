from django.contrib import admin
from .models import Category,RecurringExpense,Budget,Expense
admin.site.register(Category)
admin.site.register(RecurringExpense)
admin.site.register(Budget)
admin.site.register(Expense)
# Register your models here.
