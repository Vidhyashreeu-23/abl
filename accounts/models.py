from django.contrib.auth.models import AbstractUser
from django.db import models


class Skill(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class Interest(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    bio = models.TextField(blank=True)
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    skills = models.ManyToManyField(Skill, blank=True)
    interests = models.ManyToManyField(Interest, blank=True)
    college = models.CharField(max_length=255, blank=True)
    graduation_year = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.username
