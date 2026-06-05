from django.db import models


class Subject(models.Model):
    """
    Навчальний предмет (математика, англійська, програмування).
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ARCHIVED', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='subjects'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    
    class Meta:
        # Не може бути двох предметів з однаковою назвою в одній філії
        unique_together = ['name', 'branch']
        verbose_name_plural = 'Subjects'
    
    def __str__(self):
        return f"{self.name} ({self.branch.name})"