# Generated by Django 5.2.1 on 2025-05-12 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('attendee', '0003_rename_name_attendee_first_name_attendee_last_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='slug',
            field=models.SlugField(blank=True, unique=True),
        ),
    ]
