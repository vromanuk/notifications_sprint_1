from django.utils import timezone

from notifications_api.apps.task_scheduler.models import Task


class Scheduler:
    def __init__(self, handle, params):
        self.handle = handle
        self.params = params

    def create_task(self, launched_at):
        return Task.objects.create(
            handle=self.handle, params=self.params, launched_at=launched_at
        )

    def cancel_task(self):
        return Task.objects.filter(handle=self.handle, state=Task.State.PENDING).update(
            state=Task.State.CANCELED, finished_at=timezone.now()
        )
