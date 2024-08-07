# Generated by Django 5.0.6 on 2024-07-18 15:48

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0002_order_used_coupon"),
        ("wishlist_cart", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="shopping_cart",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                to="wishlist_cart.shoppingcart",
            ),
        ),
    ]
