# Generated by Django 5.1.2 on 2024-10-23 13:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyFavoriteDishes', '0005_favoritedish_food'),
    ]

    operations = [
        migrations.AddField(
            model_name='favoritedish',
            name='flavor',
            field=models.CharField(default='Unknown', max_length=100),
        ),
    ]
