from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

# Create your models here.
class NewDish(models.Model):
    uuid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=100)
    flavor = models.CharField(max_length=100)
    category = models.CharField(max_length=50)
    vendor_name = models.CharField(max_length=100, default="Unknown Vendor")
    price = models.IntegerField() 
    map_link = models.CharField(max_length=255, default="")
    address = models.CharField(max_length=255, default="")
    image = models.CharField(max_length=255, default="")
    is_approved = models.BooleanField(default=False)  # Status approval oleh admin
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)