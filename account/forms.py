from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class UserUpdateForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name']
        widgets = {
           'first_name': forms.TextInput(attrs={'class': 'form-control'}),
           'last_name': forms.TextInput(attrs={'class': 'form-control'}),
           'email': forms.TextInput(attrs={'class': 'form-control'}),
           'username': forms.TextInput(attrs={'class': 'form-control'}),
        }


class ChangeUserPasswordForm(PasswordChangeForm):
    old_password = forms.PasswordInput(attrs={'class': 'form-control'})
    new_password1 = forms.PasswordInput(attrs={'class': 'form-control'})
    new_password2 = forms.PasswordInput(attrs={'class': 'form-control'})
