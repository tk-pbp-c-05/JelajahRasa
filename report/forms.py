from django import forms
from .models import Report

class ReportForm(forms.ModelForm):
    class Meta:
        model = Report
        fields = ['issue_type', 'description']
        widgets = {
            'description': forms.Textarea(attrs={'placeholder': 'isi keluhan anda ...'}),
        }