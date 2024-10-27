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
    location = models.CharField(max_length=50, blank=True, null=True, default="Indonesia")
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
    average_rating = models.FloatField(default=0.0)

    def update_average_rating(self):
        from review.models import Review
        reviews = self.reviews.all()  # Get all reviews related to this food item
        if reviews.exists():
            avg_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            count = reviews.count()
            self.average_rating = round(avg_rating, 1) if avg_rating is not None else 0.0  # Round to 1 decimal
            self.rating_count = count
            self.save()
        else:
            # If there are no reviews, set average to 0 and count to 0
            self.average_rating = 0.0
            self.rating_count = 0
            self.save()