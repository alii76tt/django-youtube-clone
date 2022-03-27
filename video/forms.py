from django import forms
from .models import Comment, Video
from ckeditor.fields import RichTextField


class VideoForm(forms.ModelForm):
    class Meta:
        model = Video
        fields = [
            'title',
            'content',
            'cover_image',
            'video',
            'status'
        ]
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Video Title'}),
            'content': RichTextField()
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = [
            'comment',
        ]
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control',  'id': "exampleFormControlTextarea1", 'rows': "3", 'placeholder': 'Add comment..'}),
        }
