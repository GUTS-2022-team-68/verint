from django.contrib.auth.models import Group
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import AuthGroup


@receiver(post_save, sender=Group)
def create_auth_group(sender, instance, created, **kwargs):
    """Create the AuthGroup model when a group is created."""
    if created:
        AuthGroup.objects.create(group=instance)