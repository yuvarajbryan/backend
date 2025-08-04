from rest_framework import viewsets, permissions
from .models import Comment
from .serializers import CommentSerializer
from projects.models import Task
from accounts.models import User
from django.db import models

class IsAdminManagerOrTaskUser(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role in ['admin', 'manager']:
            return True
        # User can access if they are assigned to the task or own the project
        if obj.user == user:
            return True
        if obj.task.assigned_to == user:
            return True
        if obj.task.project.owner == user:
            return True
        return False

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all().order_by('-created_at')
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminManagerOrTaskUser]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Comment.objects.all()
        # User can see comments on tasks they are assigned to or own
        return Comment.objects.filter(
            models.Q(user=user) |
            models.Q(task__assigned_to=user) |
            models.Q(task__project__owner=user)
        ).distinct()
