from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=15, required=True)
    flat_number = forms.CharField(max_length=10, required=True)
    wing = forms.CharField(max_length=5, required=True)
    society = forms.ModelChoiceField(queryset=None, required=True)
    emergency_contact = forms.CharField(max_length=15, required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2', 'user_type', 
                 'phone', 'flat_number', 'wing', 'society', 'emergency_contact')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        from .models import Society
        self.fields['society'].queryset = Society.objects.all()
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class CustomAuthenticationForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'phone', 'flat_number', 
                 'wing', 'emergency_contact', 'profile_picture')
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control'})