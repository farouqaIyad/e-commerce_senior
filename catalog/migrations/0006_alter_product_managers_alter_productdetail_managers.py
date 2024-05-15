# Generated by Django 4.2.11 on 2024-05-13 13:44

from django.db import migrations
import django.db.models.manager


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0005_alter_product_average_rating"),
    ]

    operations = [
        migrations.AlterModelManagers(
            name="product",
            managers=[
                ("active_products", django.db.models.manager.Manager()),
            ],
        ),
        migrations.AlterModelManagers(
            name="productdetail",
            managers=[
                ("active_product_details", django.db.models.manager.Manager()),
            ],
        ),
    ]
