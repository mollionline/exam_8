from django.db import models
from django.contrib.auth import get_user_model


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(get_user_model(), related_name='profile', on_delete=models.CASCADE,
                                verbose_name='Пользователь')
    email = models.EmailField(blank=False, null=False, unique=True)

    def __str__(self):
        return f"{self.user.get_full_name()}'s Profile"
