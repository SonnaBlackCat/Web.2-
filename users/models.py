from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models


class CustomUserManager(UserManager):
    """
    Кастомний менеджер, який працює з phone замість username.
    """
    def _create_user(self, phone, password, **extra_fields):
        if not phone:
            raise ValueError('The given phone must be set')
        
        # Нормалізуємо телефон (прибираємо пробіли)
        phone = self.normalize_phone(phone)
        
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(phone, password, **extra_fields)

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(phone, password, **extra_fields)

    @classmethod
    def normalize_phone(cls, phone):
        """Нормалізація номера телефону."""
        return phone.strip() if phone else phone


class User(AbstractUser):
    """
    Кастомна модель користувача.
    Логін по номеру телефону замість email.
    """
    ROLE_CHOICES = [
        ('ADMIN', 'Administrator'),
        ('TEACHER', 'Teacher'),
    ]
    
    # Видаляємо username, використовуємо phone
    username = None
    email = models.EmailField(blank=True, null=True)
    
    # Основне поле для логіну
    phone = models.CharField(max_length=20, unique=True)
    
    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES,
        default='TEACHER'
    )
    
    # Для адміна — до яких філій він має доступ
    branches = models.ManyToManyField(
        'branches.Branch',
        blank=True,
        related_name='administrators'
    )
    
    # Для вчителя — його основна філія
    branch = models.ForeignKey(
        'branches.Branch',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='teachers'
    )
    
    # Замінюємо стандартний менеджер на кастомний
    objects = CustomUserManager()
    
    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ['first_name', 'last_name']
    
    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone})"
    
    @property
    def is_admin(self):
        return self.role == 'ADMIN'
    
    @property
    def is_teacher(self):
        return self.role == 'TEACHER'