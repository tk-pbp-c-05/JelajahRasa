from django.forms import ModelForm
from module4.models import NewDish


class NewDishForm(ModelForm):
    class Meta:
        model = NewDish
        fields = ['nama', 'rasa', 'jenis', 'nama_restoran', 'harga', 'link_gmaps', 'alamat']