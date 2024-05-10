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
            name="Wishlist",
            fields=[
                (
                    "customer",
                    models.OneToOneField(
                        on_delete=django.db.models.deletion.CASCADE,
                        primary_key=True,
                        serialize=False,
                        to="Users.customerprofile",
                    ),
                ),
                (
                    "product",
                    models.ManyToManyField(blank=True, to="catalog.productdetail"),
                ),
            ],
            options={
                "db_table": "wishlist",
            },
        ),
    ]
