from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Team

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'role', 'team', 'is_staff', 'is_active')
    list_filter = ('role', 'team', 'is_staff', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Role & Team', {'fields': ('role', 'team')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Role & Team', {'fields': ('role', 'team')}),
    )

class TeamAdmin(admin.ModelAdmin):
    list_display = ('name', 'manager', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'manager__username')

# Register your models here.
admin.site.register(User, CustomUserAdmin)
admin.site.register(Team, TeamAdmin)
