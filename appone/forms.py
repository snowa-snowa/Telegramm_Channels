from django import forms
from django.contrib.auth.models import User
from .models import Profile

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
        }

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['phone', 'age', 'description']
        widgets = {
            'phone': forms.TextInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
            'age': forms.NumberInput(attrs={
                'class': 'form-control bg-dark text-light'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control bg-dark text-light',
                'rows': 3
            }),
        }
