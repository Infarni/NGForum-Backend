from django.db import models
from django.contrib.auth.models import AbstractUser


def user_directory_path_avatar(instance, filename):
    return f'users/{instance.username}/avatar.jpg'


class UserModel(AbstractUser):
    username = models.CharField(max_length=64, unique=True)
    email = models.EmailField(unique=True)
    discription = models.TextField(max_length=1024, blank=True)
    avatar = models.ImageField(
        upload_to=user_directory_path_avatar,
        blank=True,
        default='default_avatar.jpg'
    )

    USERNAME_FIELD = 'email'
    
    REQUIRED_FIELDS = ['username']
    
    
    class Meta:
        verbose_name = 'Користувач'
        verbose_name_plural = 'Користувачі'


    def __str__(self):
        return self.username
