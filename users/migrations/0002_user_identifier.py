# Generated by Django 4.0.3 on 2022-04-17 18:45

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='identifier',
            field=models.UUIDField(default=uuid.uuid4, editable=False),
        ),
    ]