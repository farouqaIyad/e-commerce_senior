from django.dispatch import receiver
from django.db.models.signals import post_save
from .models import Order
from .tasks import (
    add_product_bought_from_supplier,
    deduct_from_products_stock,
    set_pick_up_method,
)
from notifications.tasks import notifiy_drivers


@receiver(post_save, sender=Order)
def order_completed(sender, instance, created, **kwargs):
    if not created and instance.order_status == "Deliverd":
        add_product_bought_from_supplier.delay(instance.id)
    return "done"


@receiver(post_save, sender=Order)
def order_created(sender, instance, created, **kwargs):
    if created:
        deduct_from_products_stock.delay(instance.id)
        set_pick_up_method.delay(instance.id)
        notifiy_drivers.delay()

    return "done"
