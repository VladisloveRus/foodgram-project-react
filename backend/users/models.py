from enum import unique
from operator import mod
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import UniqueConstraint
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    email = models.EmailField('email', null=False, blank=False, unique=True, max_length = 254)
    username = models.CharField('username', null=False, blank=False, max_length = 150, unique=True)
    first_name = models.CharField('first_name', null=False, blank=False, max_length = 150)
    last_name = models.CharField('last_name', null=False, blank=False, max_length = 150)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    class Meta:
        swappable = 'AUTH_USER_MODEL'
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.username


User = get_user_model()


class Follow(models.Model):
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписка',
        related_name='following',
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
        related_name='follower',
    )

    class Meta:
        verbose_name = 'Подписки'
        constraints = [
            UniqueConstraint(fields=['following', 'user'], name='unique_follow')
        ]
