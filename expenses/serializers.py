from rest_framework import serializers
from .models import Expense,Category

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ["user"]

    # def create(self,validated_data):
    #     user = self.context['request'].user 
    #     return Expense.objects.create(user=user,**validated_data)

class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = '__all__'