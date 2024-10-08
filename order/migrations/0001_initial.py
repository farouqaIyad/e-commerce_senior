# Generated by Django 5.0.6 on 2024-08-23 17:26

import django.db.models.deletion
import django.utils.timezone
import order.utils
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Users", "0001_initial"),
        ("driver", "0001_initial"),
        ("inventory", "0001_initial"),
        ("promotion", "0001_initial"),
        ("supplier", "0001_initial"),
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
                            ("Picked up", "Picked up"),
                            ("Deliverd", "Deliverd"),
                            ("Cancelled", "Cancelled"),
                        ],
                        default="Preprocessing",
                        max_length=30,
                    ),
                ),
                ("total_price", models.IntegerField()),
                (
                    "pick_up_method",
                    models.CharField(
                        choices=[("BIKE", "Bike"), ("CAR", "Car"), ("TRUCK", "Truck")],
                        max_length=9,
                    ),
                ),
                (
                    "delivery_image",
                    models.ImageField(default="orders/default.png", upload_to="orders"),
                ),
                (
                    "cart",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart",
                        to="wishlist_cart.shoppingcart",
                    ),
                ),
                (
                    "driver",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="driver.driverprofile",
                    ),
                ),
                (
                    "order_address",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="order.address"
                    ),
                ),
                (
                    "used_coupon",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="promotion.usedcoupons",
                    ),
                ),
            ],
            options={
                "db_table": "order",
            },
        ),
        migrations.CreateModel(
            name="OrderProducts",
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
                ("quantity", models.IntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="order",
                        to="order.order",
                    ),
                ),
                (
                    "products",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cart_product_detail",
                        to="inventory.productdetail",
                    ),
                ),
            ],
            options={
                "db_table": "order_products",
            },
        ),
        migrations.AddField(
            model_name="order",
            name="products",
            field=models.ManyToManyField(
                blank=True, through="order.OrderProducts", to="inventory.productdetail"
            ),
        ),
        migrations.CreateModel(
            name="ProductBoughtFromSupplier",
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
                ("products_bought", models.IntegerField(default=0)),
                (
                    "customer",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="cus",
                        to="Users.customerprofile",
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="sup",
                        to="supplier.supplierprofile",
                    ),
                ),
            ],
            options={
                "db_table": "productboughtfromsupplier",
            },
        ),
    ]
