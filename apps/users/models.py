from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

# 用户表
class Users(AbstractUser):
    avatar = models.ImageField(upload_to='avatars/')
    bio = models.TextField(blank=True)
    major = models.CharField(max_length=100, blank=True)
    grade = models.CharField(max_length=50, blank=True)
    score = models.IntegerField(default=0)
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_groups',  # 自定义 related_name
        blank=True,
        verbose_name='groups',
        help_text='The groups this user belongs to.',
        related_query_name="user",
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_permissions',  # 自定义 related_name
        blank=True,
        verbose_name='user permissions',
        help_text='Specific permissions for this user.',
        related_query_name="user",
    )

class Profile(models.Model):
    user = models.OneToOneField(Users, on_delete=models.CASCADE)
    bio = models.TextField(blank=True, verbose_name='简介')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)

    def __str__(self):
        return f"{self.user.username} 的资料"
