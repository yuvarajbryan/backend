from django.db import models
from projects.models import Task
from accounts.models import User

class TimeLog(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='timelogs')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='timelogs')
    hours = models.DecimalField(max_digits=5, decimal_places=2)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['task', 'user']
        verbose_name = 'Time Log'
        verbose_name_plural = 'Time Logs'

    def __str__(self):
        return f"{self.user.username} - {self.task.title} - {self.hours}h"
