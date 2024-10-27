from django import forms
from main.models import CustomUser

class EditProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'image_url', 'location']
        widgets = {
            'image_url': forms.URLInput(attrs={'placeholder': 'https://example.com/your-image.jpg'}),
        }
