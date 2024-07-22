# Generated by Django 5.0.6 on 2024-07-21 11:41

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_alter_categoriesbrand_brand"),
        ("order", "0007_productboughtfromsupplier"),
    ]

    operations = [
        migrations.RenameField(
            model_name="productboughtfromsupplier",
            old_name="products_bought",
            new_name="quantity",
        ),
        migrations.AddField(
            model_name="productboughtfromsupplier",
            name="product",
            field=models.ForeignKey(
                default="1",
                on_delete=django.db.models.deletion.CASCADE,
                to="catalog.productdetail",
            ),
            preserve_default=False,
        ),
    ]