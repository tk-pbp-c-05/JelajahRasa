# Generated by Django 4.2.6 on 2024-10-25 09:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0003_food_address_food_category_food_flavor_food_map_link_and_more'),
        ('MyFavoriteDishes', '0012_favoritedish_is_favorite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='favoritedish',
            name='food',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.food'),
        ),
        migrations.DeleteModel(
            name='Food',
        ),
    ]
