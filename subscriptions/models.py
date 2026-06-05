from django.db import models
from django.core.validators import MinValueValidator


class SubscriptionPlan(models.Model):
    """
    Тарифний план (ціна залежно від кількості занять на місяць).
    """
    TYPE_CHOICES = [
        ('INDIVIDUAL', 'Individual'),
        ('GROUP', 'Group'),
    ]
    
    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('ARCHIVED', 'Archived'),
    ]
    
    name = models.CharField(max_length=200)
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.CASCADE,
        related_name='subscription_plans'
    )
    plan_type = models.CharField(
        max_length=15,
        choices=TYPE_CHOICES
    )
    subjects = models.ManyToManyField(
        'subjects.Subject',
        related_name='subscription_plans'
    )
    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES,
        default='ACTIVE'
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} ({self.plan_type})"


class PricingTier(models.Model):
    """
    Ціна за заняття залежно від кількості занять в місяць.
    Приклад: 1 заняття = $25, 4 заняття = $21
    """
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE,
        related_name='pricing_tiers'
    )
    lessons_count = models.PositiveIntegerField(
        validators=[MinValueValidator(1)]
    )
    price_per_lesson = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )
    
    class Meta:
        unique_together = ['plan', 'lessons_count']
        ordering = ['lessons_count']
    
    def __str__(self):
        return f"{self.lessons_count} lessons: ${self.price_per_lesson}"
    
    @property
    def total_price(self):
        return self.lessons_count * self.price_per_lesson


class Subscription(models.Model):
    """
    Призначення тарифного плану студенту на конкретний предмет.
    """
    student = models.ForeignKey(
        'students.Student',
        on_delete=models.CASCADE,
        related_name='subscriptions'
    )
    subject = models.ForeignKey(
        'subjects.Subject',
        on_delete=models.CASCADE
    )
    plan = models.ForeignKey(
        SubscriptionPlan,
        on_delete=models.CASCADE
    )
    start_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'subject']
    
    def __str__(self):
        return f"{self.student} - {self.subject} ({self.plan.name})"