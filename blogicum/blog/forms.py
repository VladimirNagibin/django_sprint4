from django import forms
from django.utils.timezone import now

from .constants import ROWS_TEXTAREA
from .models import Comment, Post, User


class PostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = now

    class Meta:
        model = Post
        exclude = ('author',)
        widgets = {
            'text': forms.Textarea({'rows': ROWS_TEXTAREA}),
            'pub_date': forms.DateTimeInput(
                format='%Y-%m-%dT%H:%M',
                attrs={'type': 'datetime-local'}
            )
        }


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea({'rows': ROWS_TEXTAREA})
        }


class ProfileForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
