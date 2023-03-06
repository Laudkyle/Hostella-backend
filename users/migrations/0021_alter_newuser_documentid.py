# Generated by Django 4.1.7 on 2023-03-06 12:49

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0020_remove_userprofile_email_alter_newuser_documentid'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='documentId',
            field=models.UUIDField(default=uuid.UUID('081c9fb1-26db-4d57-8682-c5c5b6bef50f'), editable=False, null=True, unique=True),
        ),
    ]
