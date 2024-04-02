# Generated by Django 4.2 on 2024-04-02 20:46

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("Users", "0001_initial"),
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
                ("address_name", models.CharField(blank=True, max_length=30)),
                ("city", models.CharField(blank=True, max_length=64)),
                ("district", models.CharField(blank=True, max_length=64)),
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
            options={"db_table": "address",},
        ),
    ]
