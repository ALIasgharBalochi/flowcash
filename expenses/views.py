from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics,status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.db.models import Q
from .serializers import ExpensesSerializer,CategorySerializer,RecurringExpenseSerializer,BudgetSerializer
from .models import Expense,Category,RecurringExpense,Budget
from .filter import ExpensesFilter
from .services import calculate_expenses_sum
from datetime import date

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

class BudgetStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,uuid):
        budget = get_object_or_404(Budget,uuid=uuid)
        user = request.user

        if user != budget.user:
            return Response({"detail": "You do not have permission to access this budget."},status=status.HTTP_403_FORBIDDEN)
        
        amount_spent = calculate_expenses_sum(user,budget.created_at.date(),date.today(),budget.category)
        remaining = budget.amount - amount_spent
        percentage = (amount_spent / budget.amount * 100) if budget.amount > 0 else 0
        return Response({"amount_spent": amount_spent,"remaining": remaining,"percentage": round(percentage,2)},status=status.HTTP_200_OK)
        

            


