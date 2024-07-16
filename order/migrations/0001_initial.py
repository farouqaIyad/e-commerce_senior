# Generated by Django 5.0.6 on 2024-07-13 10:51

import django.db.models.deletion
import django.utils.timezone
import order.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Users", "0001_initial"),
        ("wishlist_cart", "0001_initial"),
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
                ("phone_number", models.CharField(max_length=10)),
                (
                    "latitude",
                    models.FloatField(
                        default=0.0, validators=[order.utils.validate_lat]
                    ),
                ),
                (
                    "longitude",
                    models.FloatField(
                        default=0.0, validators=[order.utils.validate_long]
                    ),
                ),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Users.customerprofile",
                    ),
                ),
            ],
            options={
                "db_table": "address",
                "unique_together": {("customer", "address_name")},
            },
        ),
        migrations.CreateModel(
            name="Order",
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
                    "date_created",
                    models.DateTimeField(default=django.utils.timezone.now),
                ),
                ("date_deliverd", models.DateTimeField(blank=True, null=True)),
                (
                    "order_status",
                    models.CharField(
                        choices=[
                            ("Preprocessing", "Preprocessing"),
                            ("Awaiting Pickup", "Awaiting Pickup"),
                            ("Picked up", "Picked up"),
                            ("Deliverd", "Deliverd"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="Preprocessing",
                        max_length=30,
                    ),
                ),
                (
                    "total_cost",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=10),
                ),
                (
                    "order_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="order.address"
                    ),
                ),
                (
                    "shopping_cart",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="wishlist_cart.shoppingcart",
                    ),
                ),
            ],
            options={
                "db_table": "order",
            },
        ),
    ]