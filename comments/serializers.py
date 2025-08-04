from rest_framework import serializers
from .models import Comment
from projects.models import Task
from accounts.models import User

class CommentSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    class Meta:
        model = Comment
        fields = [
            'id', 'task', 'task_title', 'user', 'user_username',
            'content', 'created_at'
        ]
        read_only_fields = ['created_at'] 