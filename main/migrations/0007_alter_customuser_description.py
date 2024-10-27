# Generated by Django 5.1.2 on 2024-10-27 15:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("main", "0006_alter_customuser_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="customuser",
            name="description",
            field=models.TextField(
                blank=True, default="No description yet.", max_length=255, null=True
            ),
        ),
    ]
