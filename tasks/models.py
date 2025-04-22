from django.db import models
from django.contrib.auth.models import User
from tasks.constants import TASK_STATUS

class Task(models.Model):
    name = models.CharField(max_length=255)
    status = models.CharField(max_length=20, choices=TASK_STATUS.items(), default='running')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tasks")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} ({self.status})"
