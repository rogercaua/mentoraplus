from django.db import models
from user.models import User

class Content(models.Model):
    TYPE_CHOICES = [
        ("roadmap", "Roadmap"),
        ("course", "Course"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    url = models.URLField(blank=True, null=True)  # URL opcional para o curso/roadmap
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contents")
    tags = models.JSONField(default=list)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

