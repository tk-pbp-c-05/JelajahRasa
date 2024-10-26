from django import forms
from .models import Comment, Reply

class CommentForm(forms.ModelForm):
    food_name = forms.CharField(required=False)

    class Meta:
        model = Comment
        fields = ['content']
        food = forms.CharField(required=False)

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']