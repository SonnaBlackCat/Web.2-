from django.contrib import admin
from .models import Branch


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address', 'status', 'created_at']
    list_filter = ['status', 'city']
    search_fields = ['name', 'city', 'address']