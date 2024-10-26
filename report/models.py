
from django.db import models
from main.models import Food
from django.contrib.auth import get_user_model

class Report(models.Model):
    ISSUE_CHOICES = [
        ('quality', 'Quality Issue'),
        ('incorrect_info', 'Incorrect Information'),
        ('out_of_stock', 'Out of Stock'),
        ('other', 'Other'),
    ]
    STATUS_CHOICES = [('pending','Pending'),
              ('approved',"Approved"),
              ('rejected',"Rejected")
              ]

    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='reports')
    reported_by = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    issue_type = models.CharField(max_length=20, choices=ISSUE_CHOICES)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True) 
    status = models.CharField(max_length=20, choices=STATUS_CHOICES,default='pending')
    

    def _str_(self):
        return f"{self.get_issue_type_display()} - {self.food.name} reported by {self.reported_by.username}"
