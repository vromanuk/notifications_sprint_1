from notifications_api.kafka.handlers.base import BaseKafkaHandler


class UserRegisteredEventHandler(BaseKafkaHandler):
    topic = "user_registered_event"

    @classmethod
    def handle(cls, body):
        print(
            "%s:%d:%d: key=%s value=%s"
            % (body.topic, body.partition, body.offset, body.key, body.value)
        )
