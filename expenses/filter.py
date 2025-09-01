from django_filters import FilterSet,NumberFilter
from .models import Expense

class ExpensesFilter(FilterSet):
    min_amount = NumberFilter(method='filter_min_amount')
    max_amount = NumberFilter(method='filter_max_amount')

    def filter_min_amount(self, queryset, name, value):
        from decimal import Decimal
        return queryset.filter(amount__gte=Decimal(value)) 

    def filter_max_amount(self,queryset, name ,value):
        from decimal import Decimal
        return queryset.filter(amount__lte=Decimal(value))

    class Meta:
        model = Expense
        fields = {
            'date': ["gte","lte"],
            'category__id': ['exact']
        }
