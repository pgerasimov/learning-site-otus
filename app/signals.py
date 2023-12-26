from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import Group
from .models import UserProfile


@receiver(post_save, sender=UserProfile)
def assign_default_group(sender, instance, created, **kwargs):
    if created:
        if instance.role == 'student':
            group, created = Group.objects.get_or_create(name='Student')
            instance.user.groups.add(group)
        elif instance.role == 'teacher':
            group, created = Group.objects.get_or_create(name='Teacher')
            instance.user.groups.add(group)