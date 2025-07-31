from django import forms
from .models import MaintenanceBill, Payment, MaintenanceType

class MaintenanceBillForm(forms.ModelForm):
    class Meta:
        model = MaintenanceBill
        fields = ('user', 'maintenance_type', 'amount', 'due_date', 'notes')
        widgets = {
            'due_date': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            field.widget.attrs.update({'class': 'form-control'})

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment
        fields = ('amount', 'payment_method', 'transaction_id', 'notes')
        widgets = {
            'notes': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            field.widget.attrs.update({'class': 'form-control'})

class MaintenanceTypeForm(forms.ModelForm):
    class Meta:
        model = MaintenanceType
        fields = ('name', 'description', 'base_amount', 'is_active')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            field.widget.attrs.update({'class': 'form-control'})