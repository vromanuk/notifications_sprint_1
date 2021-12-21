from django.db import transaction

from notifications_api.apps.users.models import User


class UserService:
    @staticmethod
    @transaction.atomic
    def create_user(username: str, email: str) -> None:
        return User.objects.create(username=username, email=email)
