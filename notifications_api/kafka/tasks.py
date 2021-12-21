import environ
from celery import shared_task
from django.core.mail import EmailMultiAlternatives

from notifications_api.apps.users.services.user import UserService

env = environ.Env()


@shared_task
def send_welcome_letter_task(username: str, send_to: str) -> None:
    subject, from_email, to = "Welcome Letter", env.str("MAILGUN_DOMAIN"), send_to
    text_content = f"{username.capitalize()} привет! Рады, что выбрали нас 😍"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()


@shared_task
def save_new_user_to_db_task(username: str, email: str) -> None:
    UserService.create_user(username, email)
