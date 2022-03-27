from django import forms
from django.contrib.auth.models import User


class UserUpdateForm(forms.ModelForm):
    username = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    last_name = forms.CharField(max_length=100, widget=forms.TextInput(
        attrs={'class': 'form-control'}))
    password = forms.CharField(
        max_length=100, label="Password", widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    repassword = forms.CharField(
        max_length=100, label="Repassword", widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'first_name',
                  'last_name', 'password', 'repassword']
