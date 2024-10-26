from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
import uuid
from django.db.models import Avg
from django.core.validators import MinValueValidator, MaxValueValidator

# Create your models here.

class CustomUserManager(BaseUserManager):
    def create_user(self, username, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_admin', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, email, password, **extra_fields)

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    is_admin = models.BooleanField(default=False)

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

    objects = CustomUserManager()

    def __str__(self):
        return self.username

    @property
    def is_regular_user(self):
        return not self.is_admin and not self.is_superuser

class Food(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=100)  
    price = models.IntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(1000000)])
    map_link = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    image = models.CharField(max_length=255, default="")
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