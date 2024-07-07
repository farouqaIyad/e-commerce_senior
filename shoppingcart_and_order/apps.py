from django.apps import AppConfig
from django.core.signals import request_finished


class ShoppingcartAndOrderConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "shoppingcart_and_order"

    def ready(self):
        from . import signals
        from .models import ShoppingCartProducts, CustomerProfile

        request_finished.connect(
            signals.shopping_cart_products_pre_save, sender=ShoppingCartProducts
        )
        request_finished.connect(
            signals.shopping_cart_product_pre_delete, sender=ShoppingCartProducts
        )
        request_finished.connect(signals.create_shopping_cart, sender=CustomerProfile)
