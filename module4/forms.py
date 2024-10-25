from django.forms import ModelForm
from module4.models import NewDish


class NewDishForm(ModelForm):
    class Meta:
        model = NewDish
        fields = ['name', 'flavor', 'category', 'vendor_name', 'price', 'map_link', 'address']