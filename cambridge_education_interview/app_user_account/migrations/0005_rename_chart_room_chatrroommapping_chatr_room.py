# Generated by Django 4.0.4 on 2025-01-14 10:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('app_user_account', '0004_remove_useraccount_location_useraccount_latitude_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='chatrroommapping',
            old_name='chart_room',
            new_name='chatr_room',
        ),
    ]