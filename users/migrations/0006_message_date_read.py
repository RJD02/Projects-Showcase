# Generated by Django 4.0 on 2022-02-24 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_message_delete_messages'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='date_read',
            field=models.DateTimeField(null=True),
        ),
    ]
