# Generated by Django 5.1.3 on 2025-01-16 15:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0020_alter_post_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='description',
            field=models.TextField(blank=True, max_length=300),
        ),
    ]
