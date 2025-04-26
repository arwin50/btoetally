from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=User.objects.all())
    
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'type', 'subject', 'amount', 'date', 'category', 'notes', 'created_at']  # Adjust the fields to match what you want to expose

    def validate_amount(self, value):
        """Ensure that the amount is not negative."""
        if value <= 0:
            raise serializers.ValidationError("Amount must be a positive number.")
        return value
