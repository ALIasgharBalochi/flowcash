from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db.models import Q
from apps.expenses.serializers import ExpensesSerializer,CategorySerializer,RecurringExpenseSerializer,BudgetSerializer
from apps.expenses.models import Expense,Category,RecurringExpense,Budget
from apps.expenses.filter import ExpensesFilter

class UserOwnedQuerySetMixin:
    @property
    def model(self):
        return self.serializer_class.Meta.model
    def get_queryset(self):
        return self.model.objects.filter(user=self.request.user)
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class ExpensesView(UserOwnedQuerySetMixin,generics.ListCreateAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ExpensesFilter


class RecurringExpenseView(UserOwnedQuerySetMixin,generics.ListCreateAPIView):
    serializer_class = RecurringExpenseSerializer
    permission_classes = [IsAuthenticated]
    
class CategoryView(UserOwnedQuerySetMixin,generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(Q(is_default=True) | Q(user=self.request.user)) 

class BudgetView(UserOwnedQuerySetMixin,generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

class ExpenseDetailView(UserOwnedQuerySetMixin,generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

class CategoryDetailView(UserOwnedQuerySetMixin,generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

class RecurringExpensesDetailView(UserOwnedQuerySetMixin,generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecurringExpenseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

class BudgetDetailsView(UserOwnedQuerySetMixin,generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
