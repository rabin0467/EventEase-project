
from django.db import models
# from django.contrib.auth.models import User
from django.conf import settings

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()

    def __str__(self):
        return self.name

class Event(models.Model):
    name= models.CharField(max_length=100)
    description = models.TextField()
    date = models.DateField()
    time = models.TimeField()
    location = models.CharField(max_length=200)
    rsvp_participants = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='rsvp_events', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    image = models.ImageField(upload_to='event_image', blank=True, null=True)

    def __str__(self):
        return self.name

