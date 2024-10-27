from django import forms
from .models import Comment, Reply
from main.models import Food

class CommentForm(forms.ModelForm):
    food = forms.ModelChoiceField(
        queryset=Food.objects.all(),
        empty_label="Select a food (optional)",
        required=False,
        widget=forms.Select(attrs={'class': 'form-select mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50'})
    )

    class Meta:
        model = Comment
        fields = ['content', 'food']
        widgets = {
            'content': forms.Textarea(attrs={
                'class': 'form-textarea mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-indigo-300 focus:ring focus:ring-indigo-200 focus:ring-opacity-50',
                'rows': 3,
                'placeholder': "What's on your mind?"
            }),
        }

class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']