# Generated by Django 5.1.3 on 2024-12-10 10:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0007_rename_username_profile_user'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
