from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete
from .models import ShoppingCartProducts


@receiver(post_save, sender=ShoppingCartProducts)
def shopping_cart_products_post_save(sender, instance, created, **kwargs):
    if instance.quantity > instance.product.stock.quantity_in_stock:
        return "there are no enough items in the stock"
    else:
        if created:
            instance.shopping_cart.total_price += (
                instance.product.price * instance.quantity
            )
            instance.shopping_cart.save()
        else:
            objects = ShoppingCartProducts.objects.filter(
                shopping_cart=instance.shopping_cart
            )
            total_cost = 0
            instance.shopping_cart.total_price = 0
            for object in objects:
                total_cost += object.product.price * object.quantity
            instance.shopping_cart.total_price = total_cost
            instance.shopping_cart.save()


@receiver(pre_delete, sender=ShoppingCartProducts)
def shopping_cart_product_pre_delete(sender, instance, **kwargs):
    product_price = instance.product.price * instance.quantity
    instance.shopping_cart.total_price -= product_price
    instance.shopping_cart.save()
