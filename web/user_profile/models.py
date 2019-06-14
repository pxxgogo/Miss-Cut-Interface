from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    email = models.EmailField(blank=True, default=None)
    files_num = models.IntegerField(default=0)
    finished_num = models.IntegerField(default=0)
