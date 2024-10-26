from django.db import models
from django.db.models import Avg
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
    price = models.IntegerField() 
    map_link = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    rating_count = models.PositiveIntegerField(default=0)

    def update_average_rating(self):
        ratings = ProductRating.objects.filter(product=self)
        if ratings.exists():
            avg_rating = ratings.aggregate(Avg('rating'))['rating__avg']
            count = ratings.count()
            self.average_rating = avg_rating
            self.rating_count = count
            self.save()

class ProductRating(models.Model):
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='ratings')
    rating = models.PositiveIntegerField()