# Generated by Django 5.1.2 on 2024-10-27 14:42

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("profilepage", "0002_alter_userprofile_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="userprofile",
            name="description",
        ),
    ]
