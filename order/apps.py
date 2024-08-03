from django.apps import AppConfig
from django.core.signals import request_finished


class OrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "order"

    def ready(self):
        from . import signals
        from .models import Order

        request_finished.connect(signals.order_completed, sender=Order)
        request_finished.connect(signals.order_created, sender=Order)
