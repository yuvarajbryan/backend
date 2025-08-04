from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from django.contrib.auth import get_user_model
from django.core.mail import send_mail
from django.conf import settings
import secrets
import string
from .models import User, Team
from .serializers import (
    UserRegistrationSerializer, UserLoginSerializer, UserDetailSerializer,
    TeamSerializer, PasswordResetRequestSerializer, PasswordResetConfirmSerializer
)
from rest_framework.permissions import IsAuthenticated, IsAdminUser

User = get_user_model()

# In-memory storage for reset tokens (in production, use Redis or database)
password_reset_tokens = {}

class UserRegistrationView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserDetailSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response(serializer.validated_data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserDetailView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        serializer = UserDetailSerializer(request.user)
        return Response(serializer.data)

class UserRoleUpdateView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, user_id):
        # Only admin and manager can update user roles
        if request.user.role not in ['admin', 'manager']:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        role = request.data.get('role')
        if role not in dict(User.ROLE_CHOICES):
            return Response({'detail': 'Invalid role.'}, status=status.HTTP_400_BAD_REQUEST)
        
        user.role = role
        user.save()
        return Response({'detail': f'User role updated to {role}.'})

class UserListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Only admin and manager can view all users
        if request.user.role not in ['admin', 'manager']:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        users = User.objects.all()
        serializer = UserDetailSerializer(users, many=True)
        return Response(serializer.data)

class UserDetailByIdView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, user_id):
        # Only admin and manager can view user details
        if request.user.role not in ['admin', 'manager']:
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserDetailSerializer(user)
        return Response(serializer.data)

class TeamListView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Only admin can view all teams
        if request.user.role != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        teams = Team.objects.all()
        serializer = TeamSerializer(teams, many=True)
        return Response(serializer.data)

class ManagerTeamView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        # Only managers can view their team
        if request.user.role != 'manager':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        # Get teams managed by this manager
        managed_teams = request.user.managed_teams.all()
        if not managed_teams.exists():
            return Response({'detail': 'No teams assigned to this manager.'}, status=status.HTTP_404_NOT_FOUND)
        
        # Get all team members from managed teams
        team_members = User.objects.filter(team__in=managed_teams)
        serializer = UserDetailSerializer(team_members, many=True)
        return Response(serializer.data)

class TeamCreateView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Only admin can create teams
        if request.user.role != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = TeamSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserTeamAssignmentView(APIView):
    permission_classes = [IsAuthenticated]
    def patch(self, request, user_id):
        # Only admin can assign users to teams
        if request.user.role != 'admin':
            return Response({'detail': 'Permission denied.'}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'detail': 'User not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        team_id = request.data.get('team')
        if not team_id:
            return Response({'detail': 'Team ID is required.'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            return Response({'detail': 'Team not found.'}, status=status.HTTP_404_NOT_FOUND)
        
        user.team = team
        user.save()
        return Response({'detail': f'User {user.username} assigned to team {team.name}.'})

class PasswordResetRequestView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = User.objects.get(email=email)
            
            # Generate a random token
            token = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(32))
            password_reset_tokens[token] = user.id
            
            # Mock email sending (in production, use Django's email backend)
            reset_url = f"http://localhost:3000/reset-password?token={token}"
            email_content = f"""
            Hello {user.username},
            
            You requested a password reset for your account.
            Click the following link to reset your password:
            
            {reset_url}
            
            If you didn't request this, please ignore this email.
            
            Best regards,
            Project Management Team
            """
            
            # In production, uncomment this:
            # send_mail(
            #     'Password Reset Request',
            #     email_content,
            #     settings.DEFAULT_FROM_EMAIL,
            #     [email],
            #     fail_silently=False,
            # )
            
            # For now, just print to console (mock)
            print(f"Password reset email sent to {email}")
            print(f"Reset URL: {reset_url}")
            
            return Response({
                'detail': 'Password reset email sent successfully.',
                'message': 'Check your email for reset instructions.'
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordResetConfirmView(APIView):
    permission_classes = [permissions.AllowAny]
    
    def post(self, request):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data['token']
            new_password = serializer.validated_data['new_password']
            
            # Check if token exists and is valid
            if token not in password_reset_tokens:
                return Response({
                    'detail': 'Invalid or expired reset token.'
                }, status=status.HTTP_400_BAD_REQUEST)
            
            user_id = password_reset_tokens[token]
            try:
                user = User.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                
                # Remove the used token
                del password_reset_tokens[token]
                
                return Response({
                    'detail': 'Password reset successfully.'
                }, status=status.HTTP_200_OK)
                
            except User.DoesNotExist:
                return Response({
                    'detail': 'User not found.'
                }, status=status.HTTP_404_NOT_FOUND)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
