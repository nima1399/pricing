# Generated by Django 5.1 on 2025-02-23 13:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("crawler", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="email",
            field=models.EmailField(max_length=254, unique=True),
        ),
    ]
