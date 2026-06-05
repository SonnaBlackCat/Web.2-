from django.contrib import admin
from .models import Subject


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'status']
    list_filter = ['status', 'branch']
    search_fields = ['name']