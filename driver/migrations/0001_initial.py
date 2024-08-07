# Generated by Django 5.0.6 on 2024-07-13 10:51

import django.contrib.auth.models
import django.db.models.deletion
import django.db.models.manager
import driver.utils
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
            name="Driver",
            fields=[],
            options={
                "proxy": True,
                "indexes": [],
                "constraints": [],
            },
            bases=("Users.user",),
            managers=[
                ("driver", django.db.models.manager.Manager()),
                ("objects", django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name="DriverProfile",
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
                ("is_approved", models.BooleanField(default=False)),
                (
                    "latitude",
                    models.FloatField(
                        default=0.0, validators=[driver.utils.validate_lat]
                    ),
                ),
                (
                    "longitude",
                    models.FloatField(
                        default=0.0, validators=[driver.utils.validate_long]
                    ),
                ),
                ("phone_number", models.CharField(max_length=15, unique=True)),
                (
                    "user",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
