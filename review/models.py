import uuid
from django.db import models
from main.models import Food
from django.contrib.auth import get_user_model

# Create your models here.
class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]

    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    food = models.ForeignKey(Food, related_name='reviews', on_delete=models.CASCADE)
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    comment = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)