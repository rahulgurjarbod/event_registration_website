from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True)
    bio = models.TextField(blank=True, null=True)
    hackathon_participant = models.BooleanField(default=True, null=True)
    avatar = models.ImageField(default='avatar.png')

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    linkedin = models.URLField(max_length=500, blank=True, null=True)
    facebook = models.URLField(max_length=500, blank=True, null=True)
    github = models.URLField(max_length=500, blank=True, null=True)
    website = models.URLField(max_length=500, blank=True, null=True)
    twitter = models.URLField(max_length=500, blank=True, null=True)
    

class Event(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    participants = models.ManyToManyField(User, blank=True, related_name='events')
    start_date = models.DateTimeField(null=True)
    end_date = models.DateTimeField(null=True)
    registration_deadline = models.DateTimeField(null=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return self.name
    

class Submission(models.Model):
    participant = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='submissions')
    event = models.ForeignKey(Event, on_delete=models.SET_NULL, null=True)
    details = models.TextField(null=True, blank=True)

    id = models.UUIDField(default=uuid.uuid4, unique=True, primary_key=True, editable=False)

    def __str__(self):
        return str(self.event) + ' --- ' + str(self.participant)