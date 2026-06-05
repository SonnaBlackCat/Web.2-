from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['phone', 'first_name', 'last_name', 'role', 'is_active', 'branch']
    list_filter = ['role', 'is_active', 'branch']
    search_fields = ['phone', 'first_name', 'last_name']
    
    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email')}),
        ('Role & Branch', {'fields': ('role', 'branch', 'branches')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'first_name', 'last_name', 'role', 'password1', 'password2'),
        }),
    )
    
    ordering = ['last_name', 'first_name']