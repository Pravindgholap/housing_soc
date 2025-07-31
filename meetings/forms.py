from django import forms
from .models import Meeting, MeetingDocument
from django.contrib.auth import get_user_model

User = get_user_model()

class MeetingForm(forms.ModelForm):
    attendees = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = Meeting
        fields = ('title', 'description', 'date', 'location', 'agenda', 'attendees')
        widgets = {
            'date': forms.DateTimeInput(attrs={'type': 'datetime-local', 'class': 'form-control'}),
            'description': forms.Textarea(attrs={'rows': 3, 'class': 'form-control'}),
            'agenda': forms.Textarea(attrs={'rows': 4, 'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            if field_name != 'attendees':
                if not hasattr(field.widget, 'attrs'):
                    field.widget.attrs = {}
                field.widget.attrs.update({'class': 'form-control'})

class MeetingMinutesForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ('minutes',)
        widgets = {
            'minutes': forms.Textarea(attrs={'rows': 8, 'class': 'form-control'}),
        }

class MeetingDocumentForm(forms.ModelForm):
    class Meta:
        model = MeetingDocument
        fields = ('title', 'file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if not hasattr(field.widget, 'attrs'):
                field.widget.attrs = {}
            field.widget.attrs.update({'class': 'form-control'})