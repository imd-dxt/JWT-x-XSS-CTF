from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
import os

class User(AbstractUser):
    ROLE_CHOICES = (
        ('user', 'Regular User'),
        ('admin', 'Administrator'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')

def user_directory_path(instance, filename):
    # Files will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return f'user_{instance.user.id}/{filename}'

class FileUpload(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='uploads')
    file = models.FileField(upload_to=user_directory_path)
    content_type = models.CharField(max_length=100)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}'s upload - {self.uploaded_at}"