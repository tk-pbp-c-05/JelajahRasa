from django.forms import ModelForm
from module4.models import NewDish


class NewDishForm(ModelForm):
    class Meta:
        model = NewDish
        fields = ['name', 'taste', 'category', 'restaurant_name', 'price', 'link_gmaps', 'address']