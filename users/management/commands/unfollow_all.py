from django.core.management.base import BaseCommand

from users.models import User


class Command(BaseCommand):
    help = "Unfollow all other users for a user"

    def add_arguments(self, parser):
        parser.add_argument("user_id", type=int, help="The id of the user")

    def handle(self, *args, **options):
        user_id = options["user_id"]
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stderr.write("User does not exist")
            return

        if not user.follows.exists():
            self.stderr.write("User following is already empty")
            return

        user.follows.clear()
        user.save()
        self.stdout.write(f"Unfollowed everyone for User id={user_id}")
