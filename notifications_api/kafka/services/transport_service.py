from typing import Type

from notifications_api.kafka.notification_transport import BaseTransport


class TransportService:
    def __init__(self, transport: Type[BaseTransport]):
        self.transport = transport

    def send_welcome_letter(
        self, username: str, send_to: str, subject: str = "", content: str = ""
    ):
        """Sends welcome message using transport"""
        self.transport.send_welcome_letter(username, send_to, subject, content)
