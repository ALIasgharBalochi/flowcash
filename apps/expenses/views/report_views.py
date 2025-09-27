from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from apps.expenses.models import Budget
from apps.expenses.services import calculate_budget_status

class BudgetStatusView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self,request,uuid):
        budget = get_object_or_404(Budget,uuid=uuid)
        user = request.user

        if user != budget.user:
            return Response({"detail": "You do not have permission to access this budget."},status=status.HTTP_403_FORBIDDEN)
        
        amount_spent,remaining,percentage = calculate_budget_status(budget,user)
        return Response({"amount_spent": amount_spent,"remaining": remaining,"percentage": round(percentage,2)},status=status.HTTP_200_OK)