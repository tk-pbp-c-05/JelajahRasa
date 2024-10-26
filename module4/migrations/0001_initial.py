# Generated by Django 5.1.2 on 2024-10-26 13:43

import django.db.models.deletion
import uuid
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='NewDish',
            fields=[
                ('uuid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, unique=True)),
                ('name', models.CharField(max_length=100)),
                ('flavor', models.CharField(max_length=100)),
                ('category', models.CharField(max_length=50)),
                ('vendor_name', models.CharField(default='Unknown Vendor', max_length=100)),
                ('price', models.IntegerField()),
                ('map_link', models.CharField(default='', max_length=255)),
                ('address', models.CharField(default='', max_length=255)),
                ('image', models.CharField(default='', max_length=255)),
                ('is_approved', models.BooleanField(default=False)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
