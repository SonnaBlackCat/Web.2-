from django.contrib import admin
from .models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'phone', 'branch', 'status']
    list_filter = ['status', 'branch']
    search_fields = ['last_name', 'first_name', 'phone', 'parent_name']