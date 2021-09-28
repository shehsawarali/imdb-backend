from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import ActivityLog, Rating, Review


@receiver(post_save, sender=Rating)
def add_rating(sender, instance, created, **kwargs):
    if created:
        action = "Rated a title"
        ActivityLog.objects.create(
            title=instance.title,
            user=instance.user,
            action=action,
            rating=instance,
        )


@receiver(post_save, sender=Review)
def add_review(sender, instance, created, **kwargs):
    if created:
        action = "Reviewed a title"
        ActivityLog.objects.create(
            title=instance.title,
            user=instance.user,
            action=action,
            review=instance,
        )
