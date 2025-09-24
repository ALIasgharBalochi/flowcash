from .models import Expense
from django.db.models import Sum
from datetime import date

def calculate_expenses_sum(user,start_date,end_date,category=None):
    filters = {
        'user': user,
        'date__gte':start_date,
        'date__lte':end_date,
    }
    if category:
        filters['category'] = category

    total_amount = Expense.objects.filter(**filters).aggregate(
        total=Sum('amount'
                  ))['total'] or 0

    return total_amount

def calculate_budget_status(budget,user):
    amount_spent = calculate_expenses_sum(user,budget.created_at.date(),date.today(),budget.category)
    remaining = budget.amount - amount_spent
    percentage = (amount_spent / budget.amount * 100) if budget.amount > 0 else 0
    return amount_spent,remaining,percentage
    
