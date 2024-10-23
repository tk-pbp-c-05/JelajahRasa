from django import forms
from .models import FavoriteDish

class FavoriteDishForm(forms.ModelForm):
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