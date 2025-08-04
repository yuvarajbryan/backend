from django.contrib.auth.models import AbstractUser
from django.db import models

class Team(models.Model):
    name = models.CharField(max_length=255)
    manager = models.ForeignKey('User', on_delete=models.CASCADE, related_name='managed_teams')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.name} (Managed by {self.manager.username})"

class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('developer', 'Developer'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='members')

    def get_team_members(self):
        """Get all team members if user is a manager"""
        if self.role == 'manager' and hasattr(self, 'managed_teams'):
            return User.objects.filter(team__in=self.managed_teams.all())
        elif self.team:
            return User.objects.filter(team=self.team)
        return User.objects.none()

    def is_team_member(self, other_user):
        """Check if another user is in the same team"""
        if self.role == 'manager':
            return other_user.team in self.managed_teams.all()
        return self.team == other_user.team
