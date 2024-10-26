# Generated by Django 5.1.2 on 2024-10-26 08:09

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('module4', '0007_remove_newdish_link_gmaps_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='newdish',
            name='id',
        ),
        migrations.AddField(
            model_name='newdish',
            name='uuid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
