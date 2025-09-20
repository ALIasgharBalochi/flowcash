from celery import shared_task
from .models import Expense,RecurringExpense
from datetime import date,datetime
from django.db.models import Q

@shared_task
def creating_recurring_costs():
        expenses = []
        recurrings = RecurringExpense.objects.select_related('category','user').filter(
            next_run_at=date.today(),
            active=True).filter(
                Q(end_date__isnull=True) | 
                Q(end_date__gte=date.today())
                )   
        if not recurrings.exists():
              return
        for recurring in recurrings:
            expenses.append(Expense(
                amount=recurring.amount,
                category=recurring.category,
                date=datetime.today(),
                description=recurring.description,
                user=recurring.user,
                recurring=recurring
                ))
            recurring.next_run_at = recurring.get_next_run()
        RecurringExpense.objects.bulk_update(recurrings,['next_run_at'])
        Expense.objects.bulk_create(expenses)

