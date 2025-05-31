from django.db import models
from user.models import User
from content.models import Content

class Recommendation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]
    
    TYPE_CHOICES = [
        ("roadmap", "Roadmap"),
        ("course", "Course"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    url = models.URLField(blank=True, null=True)# opcional 
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending", db_index=True)
    tags = models.JSONField(default=list)
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations_suggested")
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="recommendations_reviewed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
