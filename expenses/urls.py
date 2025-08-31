from django.urls import path
from .views import ExpensesView,CategoryView,ExpenseDetailView,CategoryDetailView

urlpatterns = [
    path('expenses/',ExpensesView.as_view(), name='expenses'),
    path('category/',CategoryView.as_view(), name='category'),
    path('expenses_details/<int:pk>/', ExpenseDetailView.as_view(),name='expenses_details'),
    path('category_details/<int:pk>/', CategoryDetailView.as_view(), name='category_details')
]