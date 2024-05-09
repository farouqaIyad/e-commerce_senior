# Generated by Django 4.2.11 on 2024-05-08 15:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Category",
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
                ("name", models.CharField(max_length=100, unique=True)),
                ("slug", models.SlugField(max_length=150, unique=True)),
                ("description", models.TextField()),
                ("is_active", models.BooleanField(default=True)),
                ("lft", models.PositiveIntegerField(editable=False)),
                ("rght", models.PositiveIntegerField(editable=False)),
                ("tree_id", models.PositiveIntegerField(db_index=True, editable=False)),
                ("level", models.PositiveIntegerField(editable=False)),
                (
                    "parent",
                    mptt.fields.TreeForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="children",
                        to="catalog.category",
                    ),
                ),
            ],
            options={
                "db_table": "category",
            },
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
                ("price", models.DecimalField(decimal_places=2, max_digits=10)),
                (
                    "sale_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("description", models.TextField()),
                ("is_active", models.BooleanField(default=True)),
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.category",
                    ),
                ),
            ],
            options={
                "db_table": "product",
                "ordering": ["-date_created"],
            },
        ),
        migrations.CreateModel(
            name="ProductColor",
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
                    "color",
                    models.CharField(
                        choices=[
                            ("RED", "Red"),
                            ("BLUE", "Blue"),
                            ("GREEN", "Green"),
                            ("YELLOW", "Yellow"),
                            ("ORANGE", "Orange"),
                            ("PURPLE", "Purple"),
                            ("PINK", "Pink"),
                            ("WHITE", "White"),
                            ("BLACK", "Black"),
                            ("GRAY", "Gray"),
                            ("BROWN", "Brown"),
                        ],
                        max_length=20,
                    ),
                ),
            ],
            options={
                "db_table": "colors",
            },
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
                ("sku", models.CharField(blank=True, max_length=20, unique=True)),
                ("is_active", models.BooleanField(default=True)),
                ("is_main", models.BooleanField(default=False)),
                ("color", models.ManyToManyField(to="catalog.productcolor")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product",
                        to="catalog.product",
                    ),
                ),
            ],
            options={
                "db_table": "product_detail",
            },
        ),
        migrations.CreateModel(
            name="ProductSize",
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
                    "product_size",
                    models.CharField(
                        choices=[
                            ("CLOTHES_SIZE", "Clothes_size"),
                            ("SHOES_SIZE", "Shoes_size"),
                            ("TV_SIZE", "Tv_size"),
                            ("STORAGE_SIZE", "Storage_size"),
                            ("BED_SIZE", "Bed_size"),
                        ],
                        max_length=50,
                    ),
                ),
            ],
            options={
                "db_table": "product_size",
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
                        to="catalog.productdetail",
                    ),
                ),
            ],
            options={
                "db_table": "stock",
            },
        ),
        migrations.CreateModel(
            name="Size_Value",
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
                ("value", models.CharField(max_length=255, unique=True)),
                (
                    "size",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.productsize",
                    ),
                ),
            ],
            options={
                "db_table": "size_values",
                "unique_together": {("size", "value")},
            },
        ),
        migrations.CreateModel(
            name="ProductType",
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
                ("name", models.CharField(max_length=50, unique=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.category",
                    ),
                ),
                (
                    "product_size",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.productsize",
                    ),
                ),
            ],
            options={
                "db_table": "product_type",
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
                        default="images/default.png", upload_to="images/"
                    ),
                ),
                ("is_main", models.BooleanField(default=False)),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.product",
                    ),
                ),
            ],
            options={
                "db_table": "product_image",
            },
        ),
        migrations.AddField(
            model_name="productdetail",
            name="size",
            field=models.ManyToManyField(to="catalog.size_value"),
        ),
        migrations.AddField(
            model_name="product",
            name="product_type",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="product_type",
                to="catalog.producttype",
            ),
        ),
        migrations.AddField(
            model_name="product",
            name="supplier",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
    ]