from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from production.models import Employee, Team

class Command(BaseCommand):
    help = "Add 5 users and assign them to teams"

    def handle(self, *args, **kwargs):
        users_data = [
            {"username": "kanat_user", "password": "password123", "team": Team.kanat.value},
            {"username": "govde_user", "password": "password123", "team": Team.govde.value},
            {"username": "kuyruk_user", "password": "password123", "team": Team.kuyruk.value},
            {"username": "aviyonik_user", "password": "password123", "team": Team.aviyonik.value},
            {"username": "montaj_user", "password": "password123", "team": Team.montaj.value},
        ]

        for user_data in users_data:
            user, created = User.objects.get_or_create(username=user_data["username"])
            if created:
                user.set_password(user_data["password"])
                user.save()
                self.stdout.write(f"Created user: {user_data['username']}")

            if user_data["team"]:
                Employee.objects.get_or_create(user=user, team=user_data["team"])
                self.stdout.write(f"Assigned team '{user_data['team']}' to user: {user_data['username']}")
            else:
                self.stdout.write(f"User {user_data['username']} has no team.")
