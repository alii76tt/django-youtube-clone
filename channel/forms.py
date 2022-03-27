from django import forms
from .models import Channel
from ckeditor.fields import RichTextField


class ChannelForm(forms.ModelForm):
    class Meta:
        model = Channel
        fields = [
            'channel_name',
            'slogan',
            'description',
            'avatar',
            'banner_image'
        ]
        widgets = {
           'channel_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Channel Name'}),
           'slogan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Channel Slogan'}),
           'description': RichTextField()
        }

