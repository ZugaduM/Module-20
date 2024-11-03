from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    """
    Класс, представляющий расширенный профиль пользователя, в котором
    хранится тип аутентификации, выбранный пользователем при регистрации.

    Так же в этом классе создана связь 'один-к-одному' с встроенной модель User библиотеки Django
    и опцией каскадного удаления, означающей, что при удалении пользователя все записи, связанные с ним
    также удалятся.

    Профиль содержит дополнительное поле, которое генерируется автоматически в момент регистрации
    и содержит в себе дату и время регистрации.
    """

    AUTH_CHOICES = [
        ('session', 'Session Based'),
        ('jwt', 'JWT Based'),
        ('oauth', 'OAuth Based')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    auth_method = models.CharField(max_length=10, choices=AUTH_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.auth_method}"
