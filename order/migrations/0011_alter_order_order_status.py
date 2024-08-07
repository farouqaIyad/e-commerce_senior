# Generated by Django 5.0.6 on 2024-07-21 22:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("order", "0010_alter_productboughtfromsupplier_customer_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="order",
            name="order_status",
            field=models.CharField(
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
    ]
