from django.urls import path
from .views import (
    UserRegistrationView, UserLoginView, UserDetailView, UserRoleUpdateView,
    UserListView, UserDetailByIdView, TeamListView, ManagerTeamView, TeamCreateView,
    UserTeamAssignmentView, PasswordResetRequestView, PasswordResetConfirmView
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('me/', UserDetailView.as_view(), name='user-detail'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('users/<int:user_id>/', UserDetailByIdView.as_view(), name='user-detail-by-id'),
    path('users/<int:user_id>/update-role/', UserRoleUpdateView.as_view(), name='user-role-update'),
    path('teams/', TeamListView.as_view(), name='team-list'),
    path('teams/create/', TeamCreateView.as_view(), name='team-create'),
    path('manager/team/', ManagerTeamView.as_view(), name='manager-team'),
    path('users/<int:user_id>/assign-team/', UserTeamAssignmentView.as_view(), name='user-team-assignment'),
    path('password-reset/', PasswordResetRequestView.as_view(), name='password-reset-request'),
    path('password-reset/confirm/', PasswordResetConfirmView.as_view(), name='password-reset-confirm'),
] 