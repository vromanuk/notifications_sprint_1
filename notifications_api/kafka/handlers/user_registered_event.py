from notifications_api.kafka.handlers.base import BaseKafkaHandler
from notifications_api.kafka.schemas.user_registered_event_schema import (
    UserRegisteredEventSchema,
)
from notifications_api.kafka.tasks import send_welcome_letter_task


class UserRegisteredEventHandler(BaseKafkaHandler):
    topic = "user_registered_event"

    @classmethod
    def handle(cls, body):
        event = UserRegisteredEventSchema.parse_raw(body.value)
        send_welcome_letter_task.delay(event.username, event.email)
