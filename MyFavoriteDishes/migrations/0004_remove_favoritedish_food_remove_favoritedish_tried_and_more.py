# Generated by Django 5.1.2 on 2024-10-23 04:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('MyFavoriteDishes', '0003_rename_favoritefood_favoritedish_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='favoritedish',
            name='food',
        ),
        migrations.RemoveField(
            model_name='favoritedish',
            name='tried',
        ),
        migrations.RemoveField(
            model_name='food',
            name='description',
        ),
        migrations.AddField(
            model_name='favoritedish',
            name='address',
            field=models.CharField(default='Unknown Address', max_length=255),
        ),
        migrations.AddField(
            model_name='favoritedish',
            name='category',
            field=models.CharField(default='Makanan', max_length=50),
        ),
        migrations.AddField(
            model_name='favoritedish',
            name='map_link',
            field=models.CharField(default='Unknown', max_length=255),
        ),
        migrations.AddField(
            model_name='favoritedish',
            name='name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AddField(
            model_name='favoritedish',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='favoritedish',
            name='vendor_name',
            field=models.CharField(default='Unknown', max_length=100),
        ),
        migrations.AlterField(
            model_name='food',
            name='map_link',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='food',
            name='price',
            field=models.IntegerField(),
        ),
    ]