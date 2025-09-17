from rest_framework import serializers
from .models import Expense,Category,RecurringExpense

class ExpensesSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Category.objects.all()
    )
    class Meta:
        model = Expense
        exclude = ['id','user']
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
        exclude = ['id','user']

    def update(self, instance, validated_data):
        allow_fields = ["name"]
        for field in allow_fields:
            setattr(instance,field,validated_data.get(field,getattr(instance,field)))
        instance.save()
        return instance

class RecurringExpenseSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        slug_field='uuid',
        queryset=Category.objects.all()
    )
    class Meta:
        model = RecurringExpense
        exclude = ['id','user']
        read_only_fields = ['user', 'created_at', 'updated_at']
        extra_kwargs = {
            'frequency': {'required': False},
            'anchor_date': {'required': False},
            'category': {'required': False},
            'amount': {'required': False},
            'next_run_at': {'required': False},
            'end_date': {'required': False},
            'description': {'required': False},
        }

    def validate(self, data):
        user = self.context['request'].user

        if 'amount' in data and data['amount'] <= 0:
            raise serializers.ValidationError({"amount": "Amount must be positive."})

        if 'anchor_date' in data and 'end_date' in data and data['end_date'] < data['anchor_date']:
            raise serializers.ValidationError({"end_date": "End date cannot be before anchor date."})

        if 'frequency' in data:
            if data['frequency'] not in ['daily', 'weekly', 'monthly', 'yearly']:
                raise serializers.ValidationError({
                    "frequency": "Frequency must be one of these: daily, weekly, monthly, yearly."
                })

        if 'category' in data:
            category = data['category']
            if not (category.is_default or category.user == user):
                raise serializers.ValidationError({
                    "category": "The category is not valid or does not belong to you."
                })

        return data