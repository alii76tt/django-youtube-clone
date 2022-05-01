from django import forms
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password']
        widgets = {
           'first_name': forms.TextInput(attrs={'class': 'form-control'}),
           'last_name': forms.TextInput(attrs={'class': 'form-control'}),
           'email': forms.TextInput(attrs={'class': 'form-control'}),
           'username': forms.TextInput(attrs={'class': 'form-control'}),
           'password': forms.PasswordInput(attrs={'class': 'form-control'}),
        }
