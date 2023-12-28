from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'full_name', 'company', 'role')
    list_filter = ('is_staff',)
    fieldsets = (
        (None, {'fields': ('email', 'password',)}),
        ('Personal Info', {'fields': (
            'username', 'full_name', 'company', 'role'
        )},),
        ('Permissions', {'fields': (
            'is_active', 'is_staff', 'is_superuser',
            'groups', 'user_permissions'
        )},),
        ('Important dates', {'fields': ('last_login', 'date_joined')},),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide'),
            'fields': ('email', 'password1', 'password2'),
        },),
    )
    search_fields = ('email', 'username', 'full_name', 'company', 'role')
    ordering = ('id', 'email', 'role')
