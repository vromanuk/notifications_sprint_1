import environ
from celery import shared_task
from django.core.mail import EmailMultiAlternatives

env = environ.Env()


@shared_task
def send_welcome_letter_task(username: str, send_to: str) -> None:
    subject, from_email, to = "Welcome Letter", env.str("MAILGUN_DOMAIN"), send_to
    text_content = f"{username.capitalize()} привет! Рады, что выбрали нас 😍"
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.send()
