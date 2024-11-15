# Generated by Django 5.1 on 2024-09-07 07:16

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="BaseModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("create_date", models.DateTimeField(auto_now_add=True)),
                ("update_date", models.DateTimeField(auto_now=True)),
                ("delete_date", models.DateTimeField(blank=True, null=True)),
                ("is_deleted", models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name="CrawlSource",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="crawler.basemodel",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("base_url", models.URLField()),
                ("config_string", models.TextField(blank=True, null=True)),
                ("is_valid", models.BooleanField(default=True)),
                (
                    "type",
                    models.CharField(
                        choices=[("ws", "WebSocket"), ("token", "Token")], max_length=10
                    ),
                ),
            ],
            bases=("crawler.basemodel",),
        ),
        migrations.CreateModel(
            name="ValuableGroup",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="crawler.basemodel",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
            ],
            bases=("crawler.basemodel",),
        ),
        migrations.CreateModel(
            name="ValuableObject",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="crawler.basemodel",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("description", models.TextField(blank=True, null=True)),
                (
                    "group",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crawler.valuablegroup",
                    ),
                ),
            ],
            bases=("crawler.basemodel",),
        ),
        migrations.CreateModel(
            name="CrawlConfig",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="crawler.basemodel",
                    ),
                ),
                ("helper_data", models.JSONField(blank=True, null=True)),
                ("priority", models.IntegerField(default=1)),
                (
                    "crawl_source",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crawler.crawlsource",
                    ),
                ),
                (
                    "valuable_object",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crawler.valuableobject",
                    ),
                ),
            ],
            bases=("crawler.basemodel",),
        ),
        migrations.CreateModel(
            name="ValuableRecord",
            fields=[
                (
                    "basemodel_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="crawler.basemodel",
                    ),
                ),
                ("date", models.DateTimeField()),
                ("value", models.FloatField()),
                (
                    "crawl_config",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="crawler.crawlconfig",
                    ),
                ),
            ],
            bases=("crawler.basemodel",),
        ),
    ]
