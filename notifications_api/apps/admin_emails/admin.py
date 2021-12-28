from django.contrib import admin

from .models import Email, EmailTemplate, TemplateVariable


@admin.register(EmailTemplate)
class EmailTemplateAdmin(admin.ModelAdmin):
    list_display = ("name", "description", "subject")


class TemplateVariableInline(admin.TabularInline):
    model = TemplateVariable
    extra = 1


def requeue(modeladmin, request, queryset):
    queryset.update(status=Email.STATUS_CHOICES.queued.value[0])


requeue.short_description = "Добавить в очередь"


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    inlines = (TemplateVariableInline,)
    list_display = [
        "id",
        "to",
        "subject",
        "template",
        "from_email",
        "status",
        "scheduled_time",
        "priority",
    ]
    actions = [requeue]

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        obj.queue()
