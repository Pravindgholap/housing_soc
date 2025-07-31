from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class MaintenanceType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    base_amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class MaintenanceBill(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue'),
        ('cancelled', 'Cancelled'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    maintenance_type = models.ForeignKey(MaintenanceType, on_delete=models.CASCADE)
    bill_number = models.CharField(max_length=20, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    late_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_bills')

    def __str__(self):
        return f"{self.bill_number} - {self.user.username}"

    @property
    def total_amount(self):
        return self.amount + self.late_fee

    @property
    def is_overdue(self):
        return self.due_date < timezone.now().date() and self.status == 'pending'

class Payment(models.Model):
    PAYMENT_METHODS = (
        ('cash', 'Cash'),
        ('cheque', 'Cheque'),
        ('online', 'Online Transfer'),
        ('card', 'Card Payment'),
    )

    bill = models.ForeignKey(MaintenanceBill, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHODS)
    transaction_id = models.CharField(max_length=100, blank=True)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)
    received_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Payment for {self.bill.bill_number}"