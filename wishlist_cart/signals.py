from django.dispatch import receiver
from django.db.models.signals import post_save, pre_delete, pre_save
from .models import ShoppingCartProducts, CustomerProfile, ShoppingCart, Wishlist


@receiver(post_save, sender=CustomerProfile)
def create_wishlist(sender, instance, created, **kwargs):
    if created:
        Wishlist.objects.create(customer=instance)


@receiver(post_save, sender=CustomerProfile)
def create_shopping_cart(sender, instance, created, **kwargs):
    if created:
        ShoppingCart.objects.create(customer=instance)


@receiver(post_save, sender=ShoppingCartProducts)
def shopping_cart_products_post_save(sender, created, instance, **kwargs):
    if instance.quantity > instance.product.stock.quantity_in_stock:
        return "there are no enough items in the stock"
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
