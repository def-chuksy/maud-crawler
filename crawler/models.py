from django.db import models

# Create your models here.

class URL(models.Model):
    url = models.URLField(unique=True)
    visited = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["visited"])
        ]

    def __str__(self):
        status = "visited" if self.visited else "unvisited"
        return f"{self.url} [{status}] ({self.created_at})"
