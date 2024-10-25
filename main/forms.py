from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'John'})
)
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Doe'})
)
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={'placeholder': 'example@example.com'}))

    class Meta:
        User = get_user_model()
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')
        
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username_example'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'password example'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'password example'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)  # Create user object without saving to database
        user.first_name = self.cleaned_data['first_name']  # Set first name
        user.last_name = self.cleaned_data['last_name']    # Set last name
        user.email = self.cleaned_data['email']            # Set email
        if commit:
            user.save()  # Save user to the database
        return user