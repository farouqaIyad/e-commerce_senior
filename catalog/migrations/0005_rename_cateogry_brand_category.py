# Generated by Django 5.0.6 on 2024-07-10 11:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("catalog", "0004_alter_brand_name"),
    ]

    operations = [
        migrations.RenameField(
            model_name="brand",
            old_name="cateogry",
            new_name="category",
        ),
    ]