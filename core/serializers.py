from rest_framework import serializers
from .models import AuditLog
from accounts.models import User

class AuditLogSerializer(serializers.ModelSerializer):
    user_username = serializers.CharField(source='user.username', read_only=True)
    content_type_name = serializers.CharField(source='content_type.model', read_only=True)
    
    class Meta:
        model = AuditLog
        fields = [
            'id', 'user', 'user_username', 'action', 'content_type', 'content_type_name',
            'object_id', 'object_repr', 'changes', 'ip_address', 'user_agent', 'timestamp'
        ]
        read_only_fields = ['timestamp'] 