
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
# Create your models here.

"""
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='userprofile', primary_key=True)
    profile_image = models.ImageField(upload_to='profile_images', blank=True)
    bio = models.TextField(blank=True)

    def __str__(self):
        return f'{self.user.username} profile'"""

phone_regex = RegexValidator(
    regex=r'^01[3-9]\d{8}$',
    message="Enter a valid phone number"
)
    
class CustomUser(AbstractUser):
    profile_image = models.ImageField(upload_to='profile_images', blank=True, default='profile_images/default.png')
    bio = models.TextField(blank=True)
    phone_number = models.CharField(
        blank = True,
        max_length=11,
        validators=[phone_regex]
        )

    def __str__(self):
        return self.username