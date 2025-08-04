from rest_framework import viewsets, permissions
from .models import File
from .serializers import FileSerializer
from projects.models import Task
from accounts.models import User
from django.db import models

class IsAdminManagerOrTaskUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role in ['admin', 'manager']:
            return True
        # User can access if they uploaded the file, are assigned to the task, or own the project
        if obj.uploaded_by == user:
            return True
        if obj.task.assigned_to == user:
            return True
        if obj.task.project.owner == user:
            return True
        return False

class FileViewSet(viewsets.ModelViewSet):
    queryset = File.objects.all().order_by('-uploaded_at')
    serializer_class = FileSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminManagerOrTaskUser]

    def perform_create(self, serializer):
        serializer.save(uploaded_by=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return File.objects.all()
        # User can see files on tasks they are assigned to or own
        return File.objects.filter(
            models.Q(uploaded_by=user) |
            models.Q(task__assigned_to=user) |
            models.Q(task__project__owner=user)
        ).distinct()
