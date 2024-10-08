# Generated by Django 5.0.6 on 2024-08-23 17:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("catalog", "0001_initial"),
        ("supplier", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductImageSet",
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
                ("image_set_name", models.CharField(max_length=255, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name="Product",
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
                ("slug", models.SlugField(max_length=150, unique=True)),
                ("description", models.TextField(blank=True, null=True)),
                ("is_active", models.BooleanField(default=True)),
                ("date_created", models.DateField(auto_now_add=True)),
                ("main_price", models.IntegerField(blank=True, null=True)),
                ("main_sale_price", models.IntegerField(default=0)),
                ("reviews_count", models.IntegerField(default=0)),
                (
                    "average_rating",
                    models.DecimalField(decimal_places=2, default=0.0, max_digits=3),
                ),
                ("main_image", models.CharField(max_length=255)),
                (
                    "brand",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.brand",
                    ),
                ),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.category",
                    ),
                ),
                (
                    "supplier",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="supplier.supplierprofile",
                    ),
                ),
            ],
            options={
                "db_table": "product",
            },
        ),
        migrations.CreateModel(
            name="ProductAttributeValues",
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
                ("value", models.CharField(max_length=255)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="attrs",
                        to="inventory.product",
                    ),
                ),
                (
                    "product_attr",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.productattribute",
                    ),
                ),
            ],
            options={
                "db_table": "product_attribute_values",
            },
        ),
        migrations.CreateModel(
            name="ProductImage",
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
                    "image_url",
                    models.ImageField(
                        default="products/default.png", upload_to="products"
                    ),
                ),
                (
                    "image_set_id",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.productimageset",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="ProductDetail",
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
                ("sku", models.CharField(blank=True, max_length=20)),
                ("price", models.IntegerField()),
                ("sale_price", models.IntegerField(default=0)),
                ("is_active", models.BooleanField(default=True)),
                ("is_main", models.BooleanField(default=False)),
                (
                    "color",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.productcolor",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_detail",
                        to="inventory.product",
                    ),
                ),
                (
                    "size",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.size_value",
                    ),
                ),
                (
                    "image_set_id",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="inventory.productimageset",
                    ),
                ),
            ],
            options={
                "db_table": "product_detail",
            },
        ),
        migrations.CreateModel(
            name="Stock",
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
                ("quantity_in_stock", models.IntegerField(default=0)),
                ("products_sold", models.IntegerField(default=0)),
                (
                    "product_detail",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="stock",
                        to="inventory.productdetail",
                    ),
                ),
            ],
            options={
                "db_table": "stock",
            },
        ),
        migrations.AddIndex(
            model_name="product",
            index=models.Index(fields=["slug"], name="product_slug_idx"),
        ),
    ]
