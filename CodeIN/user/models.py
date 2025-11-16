from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models


# Create your models here.
class User(AbstractUser):
    groups = models.ManyToManyField(
        Group,
        related_name='custom_user_groups',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups',
    )
    user_permissions = models.ManyToManyField(
        Permission,
        related_name='custom_user_permissions',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions',
    )
    nickname = models.CharField(max_length=50, null=True)
    question_count = models.IntegerField(default=0)
    solved_problem = models.JSONField(default=list)
