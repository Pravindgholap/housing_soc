from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User, Society

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    flat_number = forms.CharField(max_length=10, required=True)
    wing = forms.CharField(max_length=5, required=True)
    society = forms.ModelChoiceField(queryset=Society.objects.all(), required=True, empty_label="Select Society")
    emergency_contact = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 
                 'phone', 'flat_number', 'wing', 'society', 'emergency_contact')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Add helpful text for user type
        self.fields['user_type'].help_text = "Select 'Owner' if you own the flat, 'Tenant' if you rent it"
        self.fields['society'].help_text = "Select your housing society"

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'flat_number', 
                 'wing', 'society', 'emergency_contact', 'profile_picture')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})
        
        # Add help text for society field
        self.fields['society'].help_text = "Select your housing society"
        self.fields['society'].empty_label = "Select Society"