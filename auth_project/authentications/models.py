from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    AUTH_CHOICES = [
        ('session', 'Session Based'),  # Сессионная аутентификация
        ('jwt', 'JWT Based'),          # JWT аутентификация
        ('oauth', 'OAuth Based')       # OAuth аутентификация
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)  # Связь с пользователем
    auth_method = models.CharField(max_length=10, choices=AUTH_CHOICES)  # Метод аутентификации
    created_at = models.DateTimeField(auto_now_add=True)  # Дата создания

    def __str__(self):
        return f"{self.user.username} - {self.auth_method}"