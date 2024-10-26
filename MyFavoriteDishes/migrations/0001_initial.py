# Generated by Django 4.2.6 on 2024-10-26 13:01

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FavoriteDish',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=100)),
                ('flavor', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('vendor_name', models.CharField(max_length=100)),
                ('price', models.IntegerField(default=0)),
                ('map_link', models.CharField(max_length=255)),
                ('address', models.CharField(max_length=255)),
                ('is_favorite', models.BooleanField(default=True)),
            ],
        ),
    ]
