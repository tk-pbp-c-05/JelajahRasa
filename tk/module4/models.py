from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NewDish(models.Model):
    nama = models.CharField(max_length=155)
    rasa = models.CharField(max_length=6)
    jenis = models.CharField(max_length=7)
    nama_restoran = models.TextField()
    harga = models.IntegerField()
    link_gmaps = models.URLField()
    alamat = models.TextField()
    is_approved = models.BooleanField(default=False)  # Status approval oleh admin
    user = models.ForeignKey(User, on_delete=models.CASCADE)