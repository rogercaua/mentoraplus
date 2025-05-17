from django.db import models
from user.models import User
from content.models import Content

class Discussion(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="discussions")
    related_content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name="discussions")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_closed = models.BooleanField(default=False)  # Para fechar a discussão se necessário

    def __str__(self):
        return self.title
