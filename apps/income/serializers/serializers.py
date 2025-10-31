from rest_framework import serializers
from apps.income.models import Income,IncomeCategory

class IncomeSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=IncomeCategory.objects.all()
    )
    class Meta:
        model = Income
        fields = '__all__'
        read_only_fields = ['user']

class IncomeCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = IncomeCategory
        exclude = ['user']
        read_only_fields = ['is_default']