# Generated by Django 4.1.7 on 2023-03-06 12:20

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0010_alter_newuser_documentid_userprofile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='documentId',
            field=models.UUIDField(default=uuid.UUID('eb6582d2-8bf5-46ec-82fd-5204e746b87a'), editable=False, null=True, unique=True),
        ),
    ]
