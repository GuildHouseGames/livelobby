from allauth.socialaccount.models import SocialAccount
from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models
from django.db.models.signals import post_save
from django.templatetags.static import static


class LiveLobbyUserManager(UserManager):
    pass


class LiveLobbyUser(AbstractUser):
    display_name = models.CharField(max_length=30, blank=True)
    profile_picture = models.URLField(blank=True, null=True)

    # profile_picture = static('events/default_user.png')

    objects = LiveLobbyUserManager()


def save_profile(sender, instance, **kwargs):
    print(instance)
    instance.user.display_name = instance.extra_data['name']
    # uid = instance.extra_data['id']
    instance.user.profile_picture = instance.get_avatar_url()
    instance.user.save()


post_save.connect(save_profile, sender=SocialAccount)
