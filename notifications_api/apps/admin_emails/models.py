from django.db import models


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

    scheduled_at = models.DateTimeField(
        "Дата и время отправки", blank=True, null=True, db_index=True
    )
