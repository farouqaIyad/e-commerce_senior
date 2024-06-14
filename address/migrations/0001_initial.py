# Generated by Django 5.0.6 on 2024-06-12 16:15

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Address",
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
                (
                    "address_name",
                    models.CharField(blank=True, max_length=64, null=True),
                ),
                ("city", models.CharField(blank=True, max_length=64, null=True)),
                ("district", models.CharField(blank=True, max_length=64, null=True)),
                ("details", models.TextField()),
                ("phone_number", models.IntegerField()),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "address",
                "unique_together": {("customer", "address_name")},
            },
        ),
    ]
