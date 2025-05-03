from rest_framework import serializers
from .models import Transaction
from .models import MonthlyBudget

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'type', 'category', 'subject', 'amount', 'date', 'notes', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
    
    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Transaction amount cannot be negative.")
        return value

class MonthlyBudgetSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonthlyBudget
        fields = ['id', 'month', 'amount']
        
    def validate_amount(self, value):
        if value < 0:
            raise serializers.ValidationError("Transaction amount cannot be negative.")
        return value