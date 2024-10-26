from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
# Create your models here.

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensures unique email addresses
    image_url = models.CharField(max_length=255, blank=True, null=True)  # Image field

    # Add these lines to resolve the conflict
    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        related_name='customuser_set',
        related_query_name='customuser',
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        related_name='customuser_set',
        related_query_name='customuser',
    )

    def __str__(self):
        return self.username

class Food(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=100)  
    price = models.CharField(max_length=255) 
    map_link = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    image = models.CharField(max_length=255, default="")
    
    def __str__(self):
        return self.name
