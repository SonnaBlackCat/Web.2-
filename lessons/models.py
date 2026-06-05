from django.db import models
from django.core.exceptions import ValidationError


class Lesson(models.Model):
    """
    Заняття (урок).
    """
    STATUS_CHOICES = [
        ('SCHEDULED', 'Scheduled'),
        ('COMPLETED', 'Completed'),
        ('CANCELLED', 'Cancelled'),
    ]
    
    TYPE_CHOICES = [
        ('INDIVIDUAL', 'Individual'),
        ('GROUP', 'Group'),
    ]
    
    # Тип заняття
    lesson_type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES
    )
    
    # Для індивідуального заняття
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='individual_lessons'
    )
    
    # Для групового заняття
    group = models.ForeignKey(
        'groups.Group',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='lessons'
    )
    
    # Спільні поля
    teacher = models.ForeignKey(
        'users.User',
        on_delete=models.CASCADE,
        related_name='lessons'
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.CASCADE
    )
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE
    )
    
    # Час заняття
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField()
    
    status = models.CharField(
        max_length=15,
        choices=STATUS_CHOICES,
        default='SCHEDULED'
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['date', 'start_time']
    
    def __str__(self):
        if self.lesson_type == 'INDIVIDUAL':
            return f"{self.subject} with {self.student} on {self.date}"
        return f"{self.subject} with group {self.group} on {self.date}"
    
    def clean(self):
        # Перевірка: індивідуальне заняття має мати студента, групове — групу
        if self.lesson_type == 'INDIVIDUAL' and not self.student:
            raise ValidationError("Individual lesson must have a student")
        if self.lesson_type == 'GROUP' and not self.group:
            raise ValidationError("Group lesson must have a group")
        if self.lesson_type == 'INDIVIDUAL' and self.group:
            raise ValidationError("Individual lesson cannot have a group")
        if self.lesson_type == 'GROUP' and self.student:
            raise ValidationError("Group lesson cannot have an individual student")
        
        # Перевірка часу
        if self.start_time >= self.end_time:
            raise ValidationError("End time must be after start time")
    
    def save(self, *args, **kwargs):
        self.clean()
        super().save(*args, **kwargs)


class Attendance(models.Model):
    """
    Відвідуваність студента на занятті.
    """
    STATUS_CHOICES = [
        ('PRESENT', 'Present'),
        ('ABSENT', 'Absent'),
    ]
    
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name='attendance_records'
    )
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )
    note = models.TextField(blank=True)
    marked_at = models.DateTimeField(auto_now=True)
    marked_by = models.ForeignKey(
        'users.User',
        on_delete=models.SET_NULL,
        null=True
    )
    
    class Meta:
        # Один студент — один запис відвідуваності на заняття
        unique_together = ['lesson', 'student']
    
    def str(self):
        return f"{self.student} - {self.status} on {self.lesson}"