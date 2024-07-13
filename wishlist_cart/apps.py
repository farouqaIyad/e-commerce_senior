from django.apps import AppConfig
from django.core.signals import request_finished


class WishlistCartConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "wishlist_cart"

    def ready(self):
        from . import signals
        from .models import ShoppingCartProducts, CustomerProfile, Wishlist

        request_finished.connect(signals.create_wishlist, sender=CustomerProfile)
        request_finished.connect(
            signals.shopping_cart_products_post_save, sender=ShoppingCartProducts
        )
        request_finished.connect(
            signals.shopping_cart_product_pre_delete, sender=ShoppingCartProducts
        )
        request_finished.connect(signals.create_shopping_cart, sender=CustomerProfile)
