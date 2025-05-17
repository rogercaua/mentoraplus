from django.db import models
from user.models import User

class Content(models.Model):
    ROADMAP = "roadmap"
    COURSE = "course"
    TYPE_CHOICES = [
        (ROADMAP, "Roadmap"),
        (COURSE, "Course"),
    ]

    title = models.CharField(max_length=255)
    description = models.TextField()
    type = models.CharField(max_length=20, choices=TYPE_CHOICES)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="contents")
    tags = models.JSONField(default=list)  # Lista de tags (ex: ["python", "data science"])
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
