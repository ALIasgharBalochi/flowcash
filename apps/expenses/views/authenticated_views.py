from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from django.db.models import Q
from apps.expenses.serializers import ExpensesSerializer,CategorySerializer,RecurringExpenseSerializer,BudgetSerializer
from apps.expenses.models import Expense,Category,RecurringExpense,Budget
from apps.expenses.filter import ExpensesFilter

class ExpensesView(generics.ListCreateAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ExpensesFilter

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class RecurringExpenseView(generics.ListCreateAPIView):
    serializer_class = RecurringExpenseSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)
    
    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
    
class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(Q(is_default=True) | Q(user=self.request.user)) 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class BudgetView(generics.ListCreateAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
    def perform_create(self, serializer):
        return serializer.save(user=self.request.user)

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'
    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)

class RecurringExpensesDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = RecurringExpenseSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return RecurringExpense.objects.filter(user=self.request.user)

class BudgetDetails(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = BudgetSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'uuid'

    def get_queryset(self):
        return Budget.objects.filter(user=self.request.user)
