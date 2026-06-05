from django.db import models


class Branch(models.Model):
    """
    Філія навчального центру.
    """
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ARCHIVED', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    address = models.TextField()
    city = models.CharField(max_length=100)
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Branches'
    
    def __str__(self):
        return f"{self.name} ({self.city})"
    
    @property
    def is_archived(self):
        return self.status == 'ARCHIVED'