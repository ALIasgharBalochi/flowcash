from django.shortcuts import render
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status,generics 
from django.db.models import Q
from .serializers import ExpensesSerializer,CategorySerializer
from .models import Expense,Category
from .filter import ExpensesFilter

class ExpensesView(generics.ListCreateAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]
    filterset_class = ExpensesFilter

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)
    
    def perform_create(self,serializer):
        serializer.save(user=self.request.user)

class CategoryView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(Q(is_default=True) | Q(user=self.request.user)) 

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class ExpenseDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ExpensesSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Expense.objects.filter(user=self.request.user)

class CategoryDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CategorySerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Category.objects.filter(user=self.request.user)
