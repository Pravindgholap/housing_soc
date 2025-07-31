from django import forms
from .models import Complaint, ComplaintUpdate, ComplaintCategory

class ComplaintForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('title', 'description', 'category', 'priority', 'location', 'image')
        widgets = {
            'description': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
            'location': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            field.widget.attrs.update({'class': 'form-control'})

class ComplaintUpdateForm(forms.ModelForm):
    class Meta:
        model = ComplaintUpdate
        fields = ('message', 'image')
        widgets = {
            'message': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            field.widget.attrs.update({'class': 'form-control'})

class ComplaintStatusForm(forms.ModelForm):
    class Meta:
        model = Complaint
        fields = ('status', 'assigned_to')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            field.widget.attrs.update({'class': 'form-control'})