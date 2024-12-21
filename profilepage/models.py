from django.db import models
from django.contrib.auth import get_user_model
from MyFavoriteDishes.models import FavoriteDish

# Create your models here.

class UserProfile(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE, related_name='profile')

    def __str__(self):
        return f"{self.user.username}'s profile"

    def get_favorite_dishes_count(self):
        return FavoriteDish.objects.filter(user=self.user).count()
