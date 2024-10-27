from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone
from main.models import Food
import uuid
from main.models import CustomUser

User = get_user_model()

class Comment(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    food = models.ForeignKey(Food, on_delete=models.CASCADE, null=True, blank=True, related_name='comments')
    

class Reply(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='replies')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
