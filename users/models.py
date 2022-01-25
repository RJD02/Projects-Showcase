import uuid
from django.db import models
from django.contrib.auth.models import User

from django.db.models.signals import post_save, post_delete


class Profile(models.Model):
    user = models.OneToOneField(
        User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    username = models.CharField(
        max_length=200, blank=True, null=True, unique=True)
    location = models.CharField(
        max_length=200, blank=True, null=True, unique=True)
    email = models.EmailField(max_length=500, blank=True, null=True)
    about = models.CharField(max_length=200, blank=True, null=True)
    bio = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(
        null=True, blank=True, upload_to='profiles/', default='profiles/user-default.png')
    social_github = models.CharField(max_length=200, blank=True, null=True)
    social_twitter = models.CharField(max_length=200, blank=True, null=True)
    social_linkedin = models.CharField(max_length=200, blank=True, null=True)
    social_youtube = models.CharField(max_length=200, blank=True, null=True)
    social_website = models.CharField(max_length=200, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return (self.username)


class Skill(models.Model):
    owner = models.ForeignKey(
        Profile, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)

    def __str__(self) -> str:
        return (self.name)


def profile_updated(sender, instance, created, **kwargs):
    print('Profile saved')
    print(sender)
    print(created)
    print(instance)


def profile_deleted(sender, instance, **kwargs):
    print('Profile deleted')
    print(sender)
    print(instance)


post_save.connect(profile_updated, sender=Profile)
post_delete.connect(profile_deleted, sender=Profile)
