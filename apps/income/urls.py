from django.urls import path
from .views import IncomeView,IncomeCategoryView

urlpatterns = [
    path('income/',IncomeView.as_view(),name='income'),
    path('income_category/',IncomeCategoryView.as_view(),name='income_category')
]