# Generated by Django 5.0.6 on 2024-07-25 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0013_order_driver"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="delivery_image",
            field=models.ImageField(default="orders/default.png", upload_to="orders"),
        ),
    ]
