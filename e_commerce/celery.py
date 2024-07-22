from __future__ import absolute_import, unicode_literals

import os
from celery import Celery
from django.conf import settings
from celery.schedules import crontab

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "e_commerce.settings")
app = Celery("e_commerce")

app.config_from_object(settings, namespace="CELERY")
# first arg is any name you want
app.conf.beat_schedule = {
    "check promotions that are valid": {
        "task": "promotion.tasks.promotion_management",
        "schedule": crontab(hour=1, minute=00),
        #'args':()
    },
    "manage coupons": {
        "task": "promotion.tasks.coupon_management",
        "schedule": crontab(hour=16, minute=28),
    },
}
app.conf.timezone = "UTC"

app.autodiscover_tasks()
