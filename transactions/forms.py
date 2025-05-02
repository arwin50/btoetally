from django import forms
from .models import Transaction
from .models import MonthlyBudget
import datetime

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

class MonthlyBudgetForm(forms.ModelForm):
    class Meta:
        model = MonthlyBudget
        fields = ['month', 'amount']

    def clean_month(self):
        month = self.cleaned_data['month']
        if month.day != 1:
            month = month.replace(day=1)
        return month
