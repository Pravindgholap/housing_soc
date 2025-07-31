from django import forms
from .models import Transaction, TransactionCategory, Budget, BankAccount

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ('title', 'description', 'amount', 'transaction_type', 'category', 'transaction_date', 'receipt')
        widgets = {
            'transaction_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            field.widget.attrs.update({'class': 'form-control'})

class BudgetForm(forms.ModelForm):
    class Meta:
        model = Budget
        fields = ('name', 'description', 'total_budget', 'start_date', 'end_date', 'is_active')
        widgets = {
            'start_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'end_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                field.widget.attrs.update({'class': 'form-control'})

class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ('bank_name', 'account_number', 'account_type', 'ifsc_code', 'branch_name', 'current_balance', 'is_active')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                field.widget.attrs.update({'class': 'form-control'})

class TransactionCategoryForm(forms.ModelForm):
    class Meta:
        model = TransactionCategory
        fields = ('name', 'description', 'is_income', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_income', 'is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                field.widget.attrs.update({'class': 'form-control'})