from django.db import models
from user.models import User
from content.models import Content  # se quiser referenciar conteúdo

class Recommendation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20)  # "roadmap" ou "course"
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default="pending")
    suggested_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recommendations_suggested")
    reviewed_by = models.ForeignKey(User, null=True, blank=True, on_delete=models.SET_NULL, related_name="recommendations_reviewed")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
