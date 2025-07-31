from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import MaintenanceType, MaintenanceBill, Payment

@admin.register(MaintenanceType)
class MaintenanceTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'base_amount', 'is_active', 'created_at')
    list_filter = ('is_active',)
    search_fields = ('name',)

@admin.register(MaintenanceBill)
class MaintenanceBillAdmin(admin.ModelAdmin):
    list_display = ('bill_number', 'user', 'maintenance_type', 'amount', 'due_date', 'status')
    list_filter = ('status', 'maintenance_type', 'due_date')
    search_fields = ('bill_number', 'user__username', 'user__flat_number')
    readonly_fields = ('bill_number',)

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('bill', 'amount', 'payment_method', 'payment_date', 'received_by')
    list_filter = ('payment_method', 'payment_date')
    search_fields = ('bill__bill_number', 'transaction_id')