# Generated by Django 4.2.6 on 2023-12-01 11:59

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='last_activity',
            field=models.DateTimeField(default=django.utils.timezone.now, editable=False, verbose_name='last activity'),
        ),
    ]
