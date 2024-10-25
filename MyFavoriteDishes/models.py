from django.db import models
from django.contrib.auth import get_user_model
from main.models import Food
import uuid

class FavoriteDish(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    category = models.CharField(max_length=50) 
    vendor_name = models.CharField(max_length=100)
    price = models.IntegerField(default=0) 
    map_link = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    is_favorite = models.BooleanField(default=True)

    def __str__(self):
        return self.name