# Generated by Django 5.0.6 on 2024-07-18 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("promotion", "0003_coupon_time_end_coupon_time_start"),
    ]

    operations = [
        migrations.AddField(
            model_name="coupon",
            name="is_active",
            field=models.BooleanField(default=False),
        ),
    ]
