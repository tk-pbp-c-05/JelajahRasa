# Generated by Django 4.2.6 on 2024-10-25 17:32

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='food',
            name='rating_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.CreateModel(
            name='ProductRating',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.PositiveIntegerField()),
                ('food', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ratings', to='main.food')),
            ],
        ),
    ]
