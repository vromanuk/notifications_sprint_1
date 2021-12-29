import abc

from django.core.mail import EmailMultiAlternatives
from environ import environ

env = environ.Env()


class BaseTransport(abc.ABC):
    @staticmethod
    @abc.abstractmethod
    def send_welcome_letter(
        username: str, send_to: str, subject: str = "", content: str = ""
    ):
        pass


class EmailTransport(BaseTransport):
    @staticmethod
    def send_welcome_letter(
        username: str, send_to: str, subject: str = "", content: str = ""
    ):
        subject, from_email, to = (
            subject or "Welcome Letter",
            env.str("MAILGUN_DOMAIN"),
            send_to,
        )
        text_content = (
            content or f"{username.capitalize()} привет! Рады, что выбрали нас 😍"
        )
        msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
        msg.send()
