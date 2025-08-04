from rest_framework import serializers
from .models import TimeLog
from projects.models import Task
from accounts.models import User

class TimeLogSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    class Meta:
        model = TimeLog
        fields = [
            'id', 'task', 'task_title', 'user', 'user_username',
            'hours', 'description', 'created_at'
        ]
        read_only_fields = ['created_at'] 