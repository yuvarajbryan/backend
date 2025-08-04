from rest_framework import serializers
from .models import File
from projects.models import Task
from accounts.models import User

class FileSerializer(serializers.ModelSerializer):
    uploaded_by_username = serializers.CharField(source='uploaded_by.username', read_only=True)
    task_title = serializers.CharField(source='task.title', read_only=True)
    class Meta:
        model = File
        fields = [
            'id', 'task', 'task_title', 'uploaded_by', 'uploaded_by_username',
            'file', 'file_name', 'mime_type', 'file_size', 'uploaded_at'
        ]
        read_only_fields = ['uploaded_at', 'file_name', 'mime_type', 'file_size'] 