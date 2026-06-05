from django.db import models
from django.utils import timezone


class Group(models.Model):
    """
    Група студентів.
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ARCHIVED', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='groups'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    students = models.ManyToManyField(
        'students.Student',
        through='GroupMembership',
        related_name='groups'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.branch.name})"


class GroupMembership(models.Model):
    """
    Зв'язок Студент-Група з датами вступу/виходу.
    """
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE
    )
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE
    )
    joined_at = models.DateField(default=timezone.now)
    left_at = models.DateField(blank=True, null=True)
    
    class Meta:
        unique_together = ['student', 'group']
    
    def str(self):
        return f"{self.student} in {self.group}"