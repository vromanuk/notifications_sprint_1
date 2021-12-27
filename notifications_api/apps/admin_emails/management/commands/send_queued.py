from django.core.management.base import BaseCommand
from django.db.models import Q
from django.utils.timezone import now


from notifications_api.apps.admin_emails.models import Email


class Command(BaseCommand):

    def handle(self, *args, **options):
        try:
            while True:
                self._send_queued()

                if not Email.objects.filter(status=Email.STATUS_CHOICES.queued.value[0]) \
                        .filter(Q(scheduled_time__lte=now()) | Q(scheduled_time=None)).exists():
                    break
        except Exception as e:
            raise

    def _get_queued(self, batch_size=100):
        return Email.objects.filter(status=Email.STATUS_CHOICES.queued.value[0]) \
                   .select_related('template') \
                   .filter(Q(scheduled_time__lte=now()) | Q(scheduled_time=None)) \
                   .order_by('-priority')[:batch_size]

    def _send_queued(self):
        queued_emails = self._get_queued()
        total_sent, total_failed = 0, 0

        if queued_emails:
            total_sent, total_failed = self._send_bulk(queued_emails)
        return total_sent, total_failed

    def _send_bulk(self, emails):
        sent_emails = []
        failed_emails = []

        for email in emails:
            try:
                email.prepare_email_message()
            except Exception as e:
                failed_emails.append((email, e))

        for email in emails:
            try:
                email.dispatch()
                sent_emails.append(email)
            except Exception as e:
                failed_emails.append((email, e))

        email_ids = [email.id for email in sent_emails]
        Email.objects.filter(id__in=email_ids).update(status=Email.STATUS_CHOICES.sent.value[0])

        email_ids = [email.id for (email, e) in failed_emails]
        Email.objects.filter(id__in=email_ids).update(status=Email.STATUS_CHOICES.failed.value[0])

        return len(sent_emails), len(failed_emails)
