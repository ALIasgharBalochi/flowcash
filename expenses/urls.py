from django.urls import path
from .views import ExpensesView,CategoryView,ExpenseDetailView

urlpatterns = [
    path('expenses/',ExpensesView.as_view(), name='expenses'),
    path('category/',CategoryView.as_view(), name='category'),
    path('expenses_details/<int:pk>/', ExpenseDetailView.as_view(),name='expenses_details')
]