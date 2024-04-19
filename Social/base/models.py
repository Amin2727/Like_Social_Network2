from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Our user model"""

    name = models.CharField(max_length=200, null=True)
    username = models.CharField(max_length=200, unique=True, null=True, blank=True)
    email = models.EmailField(unique=True ,null=True)
    bio = models.TextField(null=True)
    avatar = models.ImageField(null=True, default="avatar.svg")
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']


class Topic(models.Model):
    """The topic model that is named when the room is created."""

    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name
    

class Room(models.Model):
    """A room model that users can use to create a room."""

    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.name
    

class Message(models.Model):
    """
    The messaging model that users can use 
    to message in the rooms they created.
    """
    
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.body[0:50]


