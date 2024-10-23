from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class NewDish(models.Model):
    name = models.CharField(max_length=155)
    taste = models.CharField(max_length=6)
    category = models.CharField(max_length=7)
    restaurant_name = models.TextField()
    price = models.IntegerField()
    link_gmaps = models.URLField()
    address = models.TextField()
    is_approved = models.BooleanField(default=False)  # Status approval oleh admin
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)