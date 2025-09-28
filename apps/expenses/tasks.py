from celery import shared_task
from .models import Expense
from .services import get_active_recurrings,build_expenses_for_recurring,update_next_run_at

@shared_task
def creating_recurring_costs():
    recurrings = get_active_recurrings()
    if not recurrings.exists():
        return
    expenses = [build_expenses_for_recurring(recurring) for recurring in recurrings ] 
    Expense.objects.bulk_create(expenses)
    update_next_run_at(recurrings)

