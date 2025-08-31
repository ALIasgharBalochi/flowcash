from rest_framework import serializers
from .models import Expense,Category

class ExpensesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Expense
        fields = '__all__'
        read_only_fields = ["user"]

    def update(self,instance,validated_data):
        allowed_fields = ['amount',"category","date","description"]
        for field in allowed_fields:
            setattr(instance,field,validated_data.get(field,getattr(instance,field)))
        instance.save()
        return instance


class CategorySerializer(serializers.ModelSerializer):
    class Meta: 
        model = Category
        fields = '__all__'

    def update(self, instance, validated_data):
        allow_fields = ["name"]
        for field in allow_fields:
            setattr(instance,field,validated_data.get(field,getattr(instance,field)))
        instance.save()
        return instance