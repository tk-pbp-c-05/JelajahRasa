from django.db import models
from django.contrib.auth.models import User
import uuid

class Food(models.Model):
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # e.g., 'Makanan'
    vendor_name = models.CharField(max_length=100)
    price = models.IntegerField()  # Adjust type as needed (e.g., IntegerField for numeric values)
    map_link = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class FavoriteDish(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    category = models.CharField(max_length=50)  # e.g., 'Makanan'
    vendor_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0)  # Adjust type as needed (e.g., IntegerField for numeric values)
    map_link = models.CharField(max_length=255)
    address = models.CharField(max_length=255)

    def __str__(self):
        return self.name