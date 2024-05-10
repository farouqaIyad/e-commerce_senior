# Generated by Django 4.2.11 on 2024-05-09 23:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("catalog", "0001_initial"),
        ("Users", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Promotion",
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
                ("name", models.CharField(max_length=255, unique=True)),
                ("description", models.TextField(blank=True)),
                ("discount_percentege", models.IntegerField()),
                ("time_start", models.DateField()),
                ("time_end", models.DateField()),
                ("is_active", models.BooleanField(default=False)),
                ("is_scheduled", models.BooleanField(default=False)),
            ],
            options={
                "db_table": "promotion",
            },
        ),
        migrations.CreateModel(
            name="ProductOnPromotion",
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
                    "product_detail_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.productdetail",
                    ),
                ),
                (
                    "promotion_id",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="promotion.promotion",
                    ),
                ),
            ],
            options={
                "db_table": "product_promotion",
            },
        ),
        migrations.CreateModel(
            name="Coupon",
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
                ("name", models.CharField(max_length=255)),
                ("coupon_code", models.CharField(max_length=10)),
                ("discount_percentege", models.IntegerField()),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="Users.supplierprofile",
                    ),
                ),
            ],
            options={
                "db_table": "coupon",
                "unique_together": {("coupon_code", "supplier")},
            },
        ),
    ]
