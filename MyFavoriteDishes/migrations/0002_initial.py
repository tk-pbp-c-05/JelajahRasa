# Generated by Django 4.2.6 on 2024-10-26 13:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('main', '0001_initial'),
        ('MyFavoriteDishes', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritedish',
            name='food',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.food'),
        ),
        migrations.AddField(
            model_name='favoritedish',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
