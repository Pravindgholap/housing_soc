from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class TransactionCategory(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    is_income = models.BooleanField(default=False)  # True for income, False for expense
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Transaction Categories"

    def __str__(self):
        return f"{self.name} ({'Income' if self.is_income else 'Expense'})"

class Transaction(models.Model):
    TRANSACTION_TYPES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    category = models.ForeignKey(TransactionCategory, on_delete=models.CASCADE)
    transaction_date = models.DateField()
    receipt = models.FileField(upload_to='receipts/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} - ₹{self.amount}"

    class Meta:
        ordering = ['-transaction_date', '-created_at']

class Budget(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    total_budget = models.DecimalField(max_digits=12, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - ₹{self.total_budget}"

    @property
    def spent_amount(self):
        return Transaction.objects.filter(
            transaction_type='expense',
            transaction_date__range=[self.start_date, self.end_date]
        ).aggregate(total=models.Sum('amount'))['total'] or 0

    @property
    def remaining_budget(self):
        return self.total_budget - self.spent_amount

    @property
    def budget_utilization_percentage(self):
        if self.total_budget > 0:
            return (self.spent_amount / self.total_budget) * 100
        return 0

class BankAccount(models.Model):
    ACCOUNT_TYPES = (
        ('savings', 'Savings'),
        ('current', 'Current'),
        ('fixed_deposit', 'Fixed Deposit'),
    )

    bank_name = models.CharField(max_length=100)
    account_number = models.CharField(max_length=20)
    account_type = models.CharField(max_length=15, choices=ACCOUNT_TYPES)
    ifsc_code = models.CharField(max_length=11)
    branch_name = models.CharField(max_length=100)
    current_balance = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.bank_name} - {self.account_number[-4:]}"

    class Meta:
        ordering = ['bank_name']