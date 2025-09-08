from celery import shared_task
from .models import Expense,RecurringExpense
from datetime import date,datetime

@shared_task
def creating_recurring_costs():
        recurrings = RecurringExpense.objects.select_related('category','user').filter(next_run_at=date.today())   
        if recurrings:
            for recurring in recurrings:
                Expense.objects.create(
                    amount=recurring.amount,
                    category=recurring.category,
                    date=datetime.today(),
                    description=recurring.description,
                    user=recurring.user,
                    )
                recurring.next_run_at = recurring.get_next_run()
                recurring.save()

