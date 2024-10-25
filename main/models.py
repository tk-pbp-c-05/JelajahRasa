from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Food(models.Model):
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=100)
    price = models.IntegerField() 
    map_link = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name