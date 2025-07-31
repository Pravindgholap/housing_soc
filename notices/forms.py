from django import forms
from .models import Notice, NoticeCategory

class NoticeForm(forms.ModelForm):
    class Meta:
        model = Notice
        fields = ('title', 'content', 'category', 'priority', 'is_pinned', 'valid_until', 'attachment')
        widgets = {
            'content': forms.Textarea(attrs={'rows': 6, 'class': 'form-control'}),
            'valid_until': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_pinned']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                field.widget.attrs.update({'class': 'form-control'})

class NoticeCategoryForm(forms.ModelForm):
    class Meta:
        model = NoticeCategory
        fields = ('name', 'color', 'is_active')
        widgets = {
            'color': forms.TextInput(attrs={'type': 'color', 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name not in ['is_active']:
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                field.widget.attrs.update({'class': 'form-control'})