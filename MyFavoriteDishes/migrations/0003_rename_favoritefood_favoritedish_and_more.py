# Generated by Django 5.1.2 on 2024-10-23 03:52

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('MyFavoriteDishes', '0002_remove_favoritefood_user'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='FavoriteFood',
            new_name='FavoriteDish',
        ),
        migrations.RenameField(
            model_name='favoritedish',
            old_name='visited',
            new_name='tried',
        ),
    ]
