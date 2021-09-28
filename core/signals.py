from django.conf import settings
from django.db.models.signals import m2m_changed, post_save
from django.dispatch import receiver

from users.models import User

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


@receiver(m2m_changed, sender=User.watchlist)
def change_watchlist(sender, instance, action, **kwargs):
    if action == "post_add":
        action = "Added a title to their watchlist"
        ActivityLog.objects.create(
            title=instance.title,
            user=instance.user,
            action=action,
        )

    elif action == "post_remove":
        action = "Removed a title from their watchlist"
        ActivityLog.objects.create(
            title=instance.title,
            user=instance.user,
            action=action,
        )


@receiver(m2m_changed, sender=User.watchlist)
def change_favorites(sender, instance, action, **kwargs):
    print("WATCHLIST SIGNAL", action)
    if action == "post_add":
        action = "Added a title to their favorites"
        ActivityLog.objects.create(
            title=instance.title,
            user=instance.user,
            action=action,
        )

    elif action == "post_remove":
        action = "Removed a title from their favorites"
        ActivityLog.objects.create(
            title=instance.title,
            user=instance.user,
            action=action,
        )
