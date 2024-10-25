from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensures unique email addresses
    image_url = models.CharField(max_length=255, blank=True, null=True)  # Image field

    def __str__(self):
        return self.username

class Food(models.Model):
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=100)  
    price = models.CharField(max_length=255)
    map_link = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name