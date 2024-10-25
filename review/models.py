from django.db import models
from main.models import Food, User

# Create your models here.
class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    food = models.ForeignKey(Food, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)