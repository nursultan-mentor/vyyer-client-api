# Generated by Django 4.1 on 2022-09-29 11:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('scan_identity', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='scan',
            old_name='identity_id',
            new_name='identity',
        ),
    ]
