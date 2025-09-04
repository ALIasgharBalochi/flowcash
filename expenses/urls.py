from django.urls import path
from .views import ExpensesView,CategoryView,ExpenseDetailView,CategoryDetailView,RecurringExpenseView,RecurringExpensesDetailView

urlpatterns = [
    path('expenses/',ExpensesView.as_view(), name='expenses'),
    path('category/',CategoryView.as_view(), name='category'),
    path('recurring_expenses/',RecurringExpenseView.as_view(),name='recurring_expenses'),
    path('expenses_details/<int:pk>/', ExpenseDetailView.as_view(),name='expenses_details'),
    path('category_details/<int:pk>/', CategoryDetailView.as_view(), name='category_details'),
    path('recurring_expenses_details/<int:pk>/',RecurringExpensesDetailView.as_view(),name='recurring_expenses_details')
]