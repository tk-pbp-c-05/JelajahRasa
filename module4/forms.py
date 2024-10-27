from django import forms
from module4.models import NewDish

# Pilihan untuk flavor dan taste
FLAVOR_CHOICES = [
    ('sweet', 'Sweet'),
    ('salty', 'Salty'),
]

CATEGORY_CHOICES = [
    ('food', 'Food'),
    ('beverage', 'Beverage'),
]

class NewDishForm(forms.ModelForm):
    flavor = forms.ChoiceField(choices=FLAVOR_CHOICES, required=True)  # Dropdown untuk flavor
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=True)  # Dropdown untuk category

    class Meta:
        model = NewDish
        fields = ['name', 'flavor', 'category', 'vendor_name', 'price', 'map_link', 'address', 'image']
