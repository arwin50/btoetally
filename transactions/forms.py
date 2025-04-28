from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['type', 'category', 'subject', 'amount', 'date', 'notes']

    type = forms.ChoiceField(choices=Transaction.TYPE_CHOICES)
    category = forms.ChoiceField(choices=Transaction.CATEGORY_CHOICES)
    subject = forms.CharField(max_length=255)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'})) 
    notes = forms.CharField(widget=forms.Textarea, required=False)
