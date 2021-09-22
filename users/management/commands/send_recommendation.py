from django.core.management.base import BaseCommand
from django.db.models import Q

from core.models import Title
from users.emails import send_recommendation_email
from users.models import User


class Command(BaseCommand):

    help = "Send title recommendations to users"

    def handle(self, *args, **options):

        email_list = User.objects.filter(email_list_preference=True)

        for user in email_list:
            recommendations = Title.objects.filter(
                Q(watchlist_set=user)
                | Q(watchlist_set__id__in=user.follows.all())
                | Q(favorites_set__id__in=user.follows.all())
            ).order_by("?")[:5]

            if recommendations.exists():
                send_recommendation_email(user, recommendations)
