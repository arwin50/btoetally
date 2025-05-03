from django.db import models

from toetally import settings 

class Transaction(models.Model):
    TYPE_CHOICES = [
        ('Expense', 'Expense'),
        ('Income', 'Income'),
    ]

    CATEGORY_CHOICES = [
        ('Food', 'Food'),
        ('Transportation', 'Transportation'),
        ('Entertainment', 'Entertainment'),
        ('Utilities', 'Utilities'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    subject = models.CharField(max_length=255)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.subject} ({self.type})"
    

class MonthlyBudget(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    month = models.DateField() 
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        unique_together = ('user', 'month')
        ordering = ['-month']

    def __str__(self):
        return f"{self.user.username} - {self.month.strftime('%B %Y')}: PHP {self.amount}"
