from django.contrib import admin
from .models import Lesson, Attendance


class AttendanceInline(admin.TabularInline):
    model = Attendance
    extra = 0


@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ['date', 'start_time', 'end_time', 'subject', 'teacher', 'lesson_type', 'status']
    list_filter = ['status', 'lesson_type', 'branch', 'date']
    search_fields = ['subjectname', 'teacherlast_name']
    inlines = [AttendanceInline]


@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ['lesson', 'student', 'status', 'marked_at']
    list_filter = ['status']