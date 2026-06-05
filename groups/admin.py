from django.contrib import admin
from .models import Group, GroupMembership


class GroupMembershipInline(admin.TabularInline):
    model = GroupMembership
    extra = 1


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'branch', 'status', 'students_count']
    list_filter = ['status', 'branch']
    search_fields = ['name']
    inlines = [GroupMembershipInline]
    
    def students_count(self, obj):
        return obj.students.count()
    students_count.short_description = 'Students'