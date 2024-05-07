from django.apps import AppConfig
from django.core.signals import request_finished


class CatalogConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "catalog"

    def ready(self):
        from . import signals
        from .models import Category, Product

        request_finished.connect(signals.category_post_save, sender=Category)
        request_finished.connect(signals.product_post_save, sender=Product)
