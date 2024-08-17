from django.db import models
from django.utils import timezone

class Task(models.Model):
    PRIORITY = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    
    user_email = models.EmailField()
    task = models.CharField(max_length=200)
    due_by = models.DateTimeField()
    priority = models.IntegerField(
        choices=PRIORITY,
        default=2,
    )
    is_urgent = models.BooleanField(default=False, blank=True, null=True)

    def __str__(self):
        return self.task

    class Meta:
        ordering = ['due_by']