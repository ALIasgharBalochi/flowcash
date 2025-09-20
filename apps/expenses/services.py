from .models import Expense
from django.db.models import Sum

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

    
