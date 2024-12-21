from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class NewDish(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=100, default="")
    price = models.IntegerField() 
    map_link = models.CharField(max_length=255, default="")
    address = models.CharField(max_length=255, default="")
    image = models.CharField(max_length=255, default="")
    is_approved = models.BooleanField(default=False)
    is_rejected = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    
    PENDING = 'Pending'
    APPROVED = 'Approved'
    REJECTED = 'Rejected'

    STATUS_CHOICES = [
        (PENDING, 'Pending'),
        (APPROVED, 'Approved'),
        (REJECTED, 'Rejected'),
    ]
    
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default=PENDING,
    )

    def __str__(self):
        return self.name
