# Generated by Django 4.2.11 on 2024-05-24 19:19

from django.db import migrations, models
import django.db.models.deletion
import django.db.models.manager
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("Users", "0001_initial"),
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
                ("is_active", models.BooleanField(default=True)),
                (
                    "image_url",
                    models.ImageField(
                        default="images/category/default.png",
                        upload_to="images/category/",
                    ),
                ),
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
            managers=[
                ("active_categories", django.db.models.manager.Manager()),
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
                ("date_created", models.DateTimeField(auto_now_add=True)),
                (
                    "main_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                (
                    "main_sale_price",
                    models.DecimalField(
                        blank=True, decimal_places=2, max_digits=10, null=True
                    ),
                ),
                ("reviews_count", models.IntegerField(default=0)),
                ("average_rating", models.FloatField(default=0)),
                (
                    "main_image",
                    models.ImageField(
                        default="images/product/default.png",
                        upload_to="images/product/",
                    ),
                ),
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
            managers=[
                ("active_products", django.db.models.manager.Manager()),
            ],
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
                ("color", models.CharField(max_length=20)),
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
                (
                    "price",
                    models.DecimalField(decimal_places=2, default=0.01, max_digits=10),
                ),
                (
                    "sale_price",
                    models.DecimalField(decimal_places=2, max_digits=10, null=True),
                ),
                ("is_active", models.BooleanField(default=True)),
                ("is_main", models.BooleanField(default=False)),
                ("color", models.ManyToManyField(to="catalog.productcolor")),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="product_detail",
                        to="catalog.product",
                    ),
                ),
            ],
            options={
                "db_table": "product_detail",
            },
            managers=[
                ("active_product_details", django.db.models.manager.Manager()),
            ],
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
                ("product_size", models.CharField(max_length=50)),
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
                        related_name="stock",
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
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="catalog.productsize",
                    ),
                ),
            ],
            options={
                "db_table": "product_type",
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
                on_delete=django.db.models.deletion.CASCADE, to="Users.supplierprofile"
            ),
        ),
    ]
