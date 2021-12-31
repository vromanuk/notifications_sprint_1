# Generated by Django 3.2.10 on 2021-12-31 08:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_emails', '0003_auto_20211228_1951'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='emailtemplate',
            options={'verbose_name': 'Email template', 'verbose_name_plural': 'Email templates'},
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='description',
            field=models.TextField(blank=True, verbose_name='description'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='name',
            field=models.CharField(max_length=254, verbose_name='template name'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='scheduled_at',
            field=models.DateTimeField(blank=True, db_index=True, null=True, verbose_name='schedule email mailing'),
        ),
        migrations.AlterField(
            model_name='emailtemplate',
            name='subject',
            field=models.CharField(max_length=254, verbose_name='template subject'),
        ),
    ]
