from django.urls import path
from .views import BudgetStatusView,BudgetDetailsView,BudgetView,ExpensesView,CategoryView,ExpenseDetailView,CategoryDetailView,RecurringExpenseView,RecurringExpensesDetailView

urlpatterns = [
    path('expenses/',ExpensesView.as_view(), name='expenses'),
    path('category/',CategoryView.as_view(), name='category'),
    path('recurring_expenses/',RecurringExpenseView.as_view(),name='recurring_expenses'),
    path('budget/',BudgetView.as_view(),name='budget'),
    path('expenses_details/<uuid:uuid>/', ExpenseDetailView.as_view(),name='expenses_details'),
    path('category_details/<uuid:uuid>/', CategoryDetailView.as_view(), name='category_details'),
    path('recurring_expenses_details/<uuid:uuid>/',RecurringExpensesDetailView.as_view(),name='recurring_expenses_details'),
    path('budget_details/<uuid:uuid>/',BudgetDetailsView.as_view(),name='budget_details'),
    path('budget/<uuid:uuid>/status/',BudgetStatusView.as_view(),name='budget_status')
]