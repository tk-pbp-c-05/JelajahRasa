from django import forms
from .models import FavoriteDish

class FavoriteDishForm(forms.ModelForm):
    FLAVOR_CHOICES = [
        ('salty', 'Salty'),
        ('sweet', 'Sweet'),
    ]
    
    flavor = forms.ChoiceField(
        choices=FLAVOR_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )

    CATEGORY_CHOICES = [
        ('food', 'Food'),
        ('beverage', 'Beverage'),
    ]

    category = forms.ChoiceField(
        choices=CATEGORY_CHOICES,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = FavoriteDish
        fields = ['name', 'flavor', 'category', 'vendor_name', 'price', 'map_link', 'address']
    
class FavoriteDishFromCatalogueForm(forms.ModelForm):
    class Meta:
        model = FavoriteDish
        fields = ['food']  # This field will be a dropdown of Food items
        widgets = {
            'food': forms.Select(attrs={'class': 'form-control'}),
        }