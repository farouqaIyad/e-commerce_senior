# Generated by Django 5.0.6 on 2024-07-13 10:51

import django.contrib.auth.models
import django.db.models.deletion
import django.db.models.manager
import supplier.utils
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Users", "0001_initial"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Supplier",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("Users.user",),
            managers=[
                ("supplier", django.db.models.manager.Manager()),
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="SupplierProfile",
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
                ("city", models.CharField(blank=True, max_length=64, null=True)),
                ("district", models.CharField(blank=True, max_length=64, null=True)),
                ("details", models.TextField(blank=True)),
                ("phone_number", models.CharField(max_length=10)),
                (
                    "latitude",
                    models.FloatField(
                        default=0.0, validators=[supplier.utils.validate_lat]
                    ),
                ),
                (
                    "longitude",
                    models.FloatField(
                        default=0.0, validators=[supplier.utils.validate_long]
                    ),
                ),
                (
                    "commercial_recored",
                    models.ImageField(
                        default="commercial_records/default.png",
                        upload_to="commercial_records",
                    ),
                ),
                ("is_approved", models.BooleanField(default=False)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "db_table": "supplier",
            },
        ),
    ]
