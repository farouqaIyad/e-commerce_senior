from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Order
from .tasks import add_product_bought_from_supplier, deduct_from_products_stock


@receiver(post_save, sender=Order)
def order_completed(sender, instance, created, **kwargs):
    if not created and instance.order_status == "Deliverd":
        add_product_bought_from_supplier.delay(instance.id)
    return "done"


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        deduct_from_products_stock.delay(instance.id)
    return "done"
