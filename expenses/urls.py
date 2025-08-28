from django.urls import path
from .views import ExpensesView,CategoryView

urlpatterns = [
    path('expenses/',ExpensesView.as_view(), name='expenses'),
    path('category/',CategoryView.as_view(), name='category')
]