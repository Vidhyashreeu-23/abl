from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Club, Membership


@receiver(post_save, sender=Club)
def add_creator_as_president(sender, instance, created, **kwargs):
    if created and instance.created_by:
        Membership.objects.get_or_create(
            user=instance.created_by,
            club=instance,
            defaults={'role': 'president'},
        )
