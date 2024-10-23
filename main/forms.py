from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class CustomUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'John'})
)
    last_name = forms.CharField(max_length=30, required=True, widget=forms.TextInput(attrs={'placeholder': 'Doe'})
)
    phone_number = forms.CharField(max_length=15, required=True, widget=forms.TextInput(attrs={'placeholder': '1234567890'})
)  
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password example'}), label="Password")
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={'placeholder': 'Password example'}), label="Password confirmation")

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone_number', 'password1', 'password2')
        
        widgets = {
            'username': forms.TextInput(attrs={'placeholder': 'username_example'}),
            'password1': forms.PasswordInput(attrs={'placeholder': 'password example'}),
            'password2': forms.PasswordInput(attrs={'placeholder': 'password example'}),
        }
        
    def save(self, commit=True):
        user = super().save(commit=False)  # Create user object without saving to database
        user.first_name = self.cleaned_data['first_name']  # Set first name
        user.last_name = self.cleaned_data['last_name']    # Set last name
        if commit:
            user.save()  # Save user to the database
        return user

    def clean_phone_number(self):
        # Get the phone number from cleaned_data
        phone_number = self.cleaned_data.get('phone_number')

        # Validation logic
        if not phone_number.isdigit():  # Check if it contains only digits
            raise forms.ValidationError("Phone number must contain only digits.")
        if len(phone_number) < 10 or len(phone_number) > 15:  # Check length
            raise forms.ValidationError("Phone number must be between 10 and 15 digits long.")

        # If the validation passes, return the cleaned value
        return phone_number