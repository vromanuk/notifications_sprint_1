from enum import Enum

from django.core.mail import EmailMessage, EmailMultiAlternatives
from django.db import models
from django.template import Context, Template
from jsonfield import JSONField


class Email(models.Model):
    class PRIORITY_CHOICES(Enum):
        low = (0, "low")
        medium = (1, "medium")
        high = (2, "high")
        now = (3, "now")

    class STATUS_CHOICES(Enum):
        failed = (0, "failed")
        queued = (1, "queued")
        sent = (2, "sent")

    # todo: set default to?
    # make non editable?
    from_email = models.CharField(verbose_name="From email", max_length=254)
    to = models.TextField("Кому", help_text="список получателей через запятую")
    cc = models.TextField(
        "Копия", help_text="список получателей через запятую", blank=True
    )
    bcc = models.TextField(
        "Скрытая копия", help_text="список получателей через запятую", blank=True
    )

    template = models.ForeignKey(
        "EmailTemplate",
        verbose_name="Шаблон",
        null=True,
        blank=True,
        help_text="При выбранном шаблоне, поля с html и темой письма не будут использованы",
        on_delete=models.CASCADE,
    )

    subject = models.CharField(verbose_name="Тема", max_length=989, blank=True)
    message = models.TextField("Сообщение", blank=True)

    html_message = models.TextField(
        verbose_name="HTML контент",
        blank=True,
        help_text="Используется, если шаблон НЕ выбран",
    )
    created = models.DateTimeField(auto_now_add=True, db_index=True)
    last_updated = models.DateTimeField(db_index=True, auto_now=True)
    scheduled_time = models.DateTimeField(
        "Дата и время отправки", blank=True, null=True, db_index=True
    )
    headers = JSONField("Заголовки", blank=True, null=True)
    status = models.PositiveSmallIntegerField(
        "Статус",
        choices=[x.value for x in STATUS_CHOICES],
        db_index=True,
        blank=True,
        null=True,
    )
    priority = models.PositiveSmallIntegerField(
        "Приоритет", choices=[x.value for x in PRIORITY_CHOICES], blank=True, null=True
    )

    send_now = models.BooleanField(verbose_name="Отправить сразу", default=False)

    class Meta:
        verbose_name = "Письмо"
        verbose_name_plural = "Письма"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._cached_email_message = None

    def email_message(self):
        """
        Returns Django EmailMessage object for sending.
        """
        if self._cached_email_message:
            return self._cached_email_message

        return self.prepare_email_message()

    def _get_context(self):
        context = {}
        for var in self.templatevariable_set.all().filter(email=self):
            context[var.name] = var.value
        return Context(context)

    def prepare_email_message(self):
        message = self.message
        if self.template is not None:
            _context = self._get_context()
            subject = self.template.render_subject(_context)
            html_message = self.template.render_html_text(_context)
        else:
            subject = self.subject
            html_message = self.html_message

        # TODO: check to, bcc, cc
        if html_message:
            msg = EmailMultiAlternatives(
                subject=subject,
                body=message,
                from_email=self.from_email,
                to=self.to.split(","),
                bcc=self.bcc,
                cc=self.cc,
                headers=self.headers,
            )
            msg.attach_alternative(html_message, "text/html")
        else:
            msg = EmailMessage(
                subject=subject,
                body=message,
                from_email=self.from_email,
                to=self.to.split(","),
                bcc=self.bcc,
                cc=self.cc,
                headers=self.headers,
            )

        self._cached_email_message = msg
        return msg

    def dispatch(self):
        try:
            email_message = self.email_message()
            email_message.send()
            status = Email.STATUS_CHOICES.sent.value[0]
        except Exception as e:
            raise e
        else:
            self.status = status
            self.save(update_fields=["status"])

    def __str__(self):
        return str(self.from_email) + " -> " + str(self.to) + " (" + self.subject + ")"

    def queue(self):
        self.status = self.STATUS_CHOICES.queued.value[0]
        self.save()


class EmailTemplate(models.Model):
    class Meta:
        verbose_name = "Шаблон письма"
        verbose_name_plural = "Шаблоны писем"

    name = models.CharField(verbose_name="Название шаблона", max_length=254)

    description = models.TextField(verbose_name="Описание", blank=True)

    subject = models.CharField(
        verbose_name="Тема",
        max_length=254,
        blank=False,
    )

    email_html_text = models.TextField(
        verbose_name="HTML",
        blank=True,
    )

    def render_html_text(self, context):
        template = Template(self.email_html_text)
        return template.render(context)

    def render_subject(self, context):
        template = Template(self.subject)
        return template.render(context)

    def __str__(self):
        return self.name


class TemplateVariable(models.Model):
    class Meta:
        verbose_name = "Template variable"
        verbose_name_plural = "Template variables"

    email = models.ForeignKey("Email", null=True, blank=True, on_delete=models.CASCADE)

    name = models.CharField(
        verbose_name="Название переменной", max_length=254, blank=False
    )

    value = models.TextField(verbose_name="Значение переменной", blank=True)

    def __str__(self):
        return self.name
