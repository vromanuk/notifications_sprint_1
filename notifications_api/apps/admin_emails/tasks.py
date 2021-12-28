from celery import shared_task
from django.core.mail import EmailMultiAlternatives
from django.template import Context
from django.utils import timezone

from config.settings.base import env
from notifications_api.apps.admin_emails.models import EmailTemplate
from notifications_api.apps.admin_emails.utils import render_html_text, render_subject
from notifications_api.apps.task_scheduler.scheduler import Scheduler
from notifications_api.apps.users.models import User


@shared_task
def send_bulk_emails_task(**kwargs):
    for user in User.objects.all():
        scheduler = Scheduler(
            send_bulk_emails,
            params={
                "user": user.username,
                "email": user.email,
                "template_id": kwargs["template_id"],
            },
        )
        scheduler.create_task(timezone.now())


@shared_task
def schedule_send_bulk_emails_task(**kwargs):
    for user in User.objects.all():
        scheduler = Scheduler(
            send_bulk_emails,
            params={
                "user": user.username,
                "email": user.email,
                "template_id": kwargs["template_id"],
            },
        )
        scheduler.create_task(kwargs["launched_at"])


@shared_task
def send_bulk_emails(**kwargs):
    try:
        template = EmailTemplate.objects.get(kwargs["template_id"])
    except EmailTemplate.DoesNotExist:
        raise ValueError(f"There is no such template_id `{kwargs['template_id']}`")
    ctx = Context()
    subject, from_email, to = (
        render_subject(ctx, template.subject),
        env.str("MAILGUN_DOMAIN"),
        kwargs["email"],
    )
    html_message = render_html_text(ctx, template.email_html_text)
    msg = EmailMultiAlternatives(
        subject=subject,
        body="",
        from_email=from_email,
        to=to,
    )
    msg.attach_alternative(html_message, "text/html")
    msg.send()
