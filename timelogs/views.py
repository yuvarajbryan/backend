from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.db import IntegrityError
from .models import TimeLog
from .serializers import TimeLogSerializer
from accounts.models import User

class IsAdminManagerOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role in ['admin', 'manager']:
            return True
        return obj.user == user

class TimeLogViewSet(viewsets.ModelViewSet):
    queryset = TimeLog.objects.all().order_by('-created_at')
    serializer_class = TimeLogSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminManagerOrOwner]

    def perform_create(self, serializer):
        try:
            # Check if user has already logged time for this task
            existing_log = TimeLog.objects.filter(
                task=serializer.validated_data['task'],
                user=self.request.user
            ).first()
            
            if existing_log:
                raise IntegrityError("You have already logged time for this task.")
            
            serializer.save(user=self.request.user)
        except IntegrityError as e:
            raise IntegrityError("You have already logged time for this task.")

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return TimeLog.objects.all()
        return TimeLog.objects.filter(user=user)
