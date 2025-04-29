from rest_framework import serializers
from .models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ['id', 'user', 'type', 'category', 'subject', 'amount', 'date', 'notes', 'created_at']
        read_only_fields = ['id', 'user', 'created_at']
