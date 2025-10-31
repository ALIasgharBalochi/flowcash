from django.shortcuts import render
from django.db.models import Q
from rest_framework.generics import ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from apps.income.serializers import IncomeSerializer,IncomeCategorySerializer
from apps.income.models import Income,IncomeCategory
from common.mixins.UserMixins import UserOwnedQuerySetMixin

class IncomeView(UserOwnedQuerySetMixin,ListCreateAPIView):
    permission_classes = [IsAuthenticated] 
    serializer_class = IncomeSerializer

class IncomeCategoryView(UserOwnedQuerySetMixin,ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = IncomeCategorySerializer

    def get_queryset(self):
        return IncomeCategory.objects.filter(Q(is_default=True) | Q(user=self.request.user))