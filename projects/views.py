from rest_framework import viewsets, permissions
from rest_framework.exceptions import PermissionDenied
from .models import Project, Task
from .serializers import ProjectSerializer, ProjectDetailSerializer, TaskSerializer
from accounts.models import User

class IsAdminManagerOrOwner(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        user = request.user
        if user.role == 'admin':
            return True
        if user.role == 'manager':
            # Managers can only access their team members' tasks
            if hasattr(obj, 'assigned_to'):
                return user.is_team_member(obj.assigned_to)
            return True
        if hasattr(obj, 'owner'):
            return obj.owner == user
        if hasattr(obj, 'assigned_to'):
            return obj.assigned_to == user
        return False

class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.all().order_by('-created_at')
    serializer_class = ProjectSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminManagerOrOwner]

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return ProjectDetailSerializer
        return ProjectSerializer

    def perform_create(self, serializer):
        # Only admins can create projects
        if self.request.user.role != 'admin':
            raise PermissionDenied("Only admins can create projects.")
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'manager']:
            return Project.objects.all()
        return Project.objects.filter(owner=user)

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all().order_by('-created_at')
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdminManagerOrOwner]

    def perform_create(self, serializer):
        user = self.request.user
        
        # If it's a manager, check if they're assigning to their team member
        if user.role == 'manager':
            assigned_to_id = serializer.validated_data.get('assigned_to')
            if assigned_to_id:
                try:
                    assigned_user = User.objects.get(id=assigned_to_id)
                    if not user.is_team_member(assigned_user):
                        raise PermissionDenied("You can only assign tasks to your team members.")
                except User.DoesNotExist:
                    raise PermissionDenied("User not found.")
        
        serializer.save()

    def get_queryset(self):
        user = self.request.user
        if user.role == 'admin':
            return Task.objects.all()
        elif user.role == 'manager':
            # Managers can only see tasks assigned to their team members
            team_members = user.get_team_members()
            return Task.objects.filter(assigned_to__in=team_members)
        return Task.objects.filter(assigned_to=user)
