# Generated by Django 5.1.2 on 2024-10-23 13:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyFavoriteDishes', '0008_food_flavor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='food',
            name='id',
            field=models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
        ),
    ]
