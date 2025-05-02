from rest_framework import serializers
from .models import Transaction
from .models import MonthlyBudget

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'type', 'category', 'subject', 'amount', 'date', 'notes', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']

class MonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudget
        fields = ['id', 'month', 'amount']