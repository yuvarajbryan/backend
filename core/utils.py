from django.contrib.contenttypes.models import ContentType
from .models import AuditLog

def log_audit_action(user, action, instance, changes=None, request=None):
    """
    Log an audit action for any model instance.
    
    Args:
        user: The user performing the action
        action: 'create', 'update', or 'delete'
        instance: The model instance being acted upon
        changes: Dictionary of field changes (for updates)
        request: HTTP request object (for IP and user agent)
    """
    content_type = ContentType.objects.get_for_model(instance)
    
    # Get IP address and user agent from request
    ip_address = None
    user_agent = ''
    if request:
        ip_address = get_client_ip(request)
        user_agent = request.META.get('HTTP_USER_AGENT', '')
    
    AuditLog.objects.create(
        user=user,
        action=action,
        content_type=content_type,
        object_id=instance.pk,
        object_repr=str(instance),
        changes=changes or {},
        ip_address=ip_address,
        user_agent=user_agent
    )

def get_client_ip(request):
    """Extract client IP address from request."""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip 