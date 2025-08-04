from rest_framework import serializers
from .models import Project, Task
from accounts.models import User

class TaskSerializer(serializers.ModelSerializer):
    assigned_to_username = serializers.CharField(source='assigned_to.username', read_only=True)
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'project', 'assigned_to', 'assigned_to_username',
            'status', 'due_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ProjectSerializer(serializers.ModelSerializer):
    owner_username = serializers.CharField(source='owner.username', read_only=True)
    class Meta:
        model = Project
        fields = [
            'id', 'name', 'description', 'owner', 'owner_username',
            'start_date', 'end_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class ProjectDetailSerializer(ProjectSerializer):
    tasks = TaskSerializer(many=True, read_only=True, source='tasks')
    class Meta(ProjectSerializer.Meta):
        fields = ProjectSerializer.Meta.fields + ['tasks'] 