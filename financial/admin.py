from django.contrib import admin
from .models import TransactionCategory, Transaction, Budget, BankAccount

@admin.register(TransactionCategory)
class TransactionCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_income', 'is_active', 'created_at')
    list_filter = ('is_income', 'is_active')
    search_fields = ('name',)

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ('title', 'amount', 'transaction_type', 'category', 'transaction_date', 'created_by')
    list_filter = ('transaction_type', 'category', 'transaction_date', 'created_at')
    search_fields = ('title', 'description', 'created_by__username')
    readonly_fields = ('created_at', 'updated_at')

@admin.register(Budget)
class BudgetAdmin(admin.ModelAdmin):
    list_display = ('name', 'total_budget', 'start_date', 'end_date', 'is_active', 'created_by')
    list_filter = ('is_active', 'start_date', 'end_date')
    search_fields = ('name', 'created_by__username')

@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ('bank_name', 'account_number', 'account_type', 'current_balance', 'is_active')
    list_filter = ('account_type', 'is_active', 'bank_name')
    search_fields = ('bank_name', 'account_number', 'branch_name')