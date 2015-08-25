from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):

    """Author: Aly Yakan"""
    comment = forms.CharField(widget=forms.Textarea)

    class Meta:
        model = Comment
        exclude = ('likes_count', 'dislikes_count', 'content_type', 'object_id',
                   'content_object')
