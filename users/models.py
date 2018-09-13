from django.db import models
from django.contrib.auth.models import AbstractUser, UserManager

class LiveLobbyUserManager(UserManager):
    pass

class LiveLobbyUser(AbstractUser):
    display_name = models.CharField(max_length=30, blank=True)
    
    objects = LiveLobbyUserManager()
