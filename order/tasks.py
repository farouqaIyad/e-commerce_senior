from celery import shared_task
from .models import ProductBoughtFromSupplier, SupplierProfile, Order, OrderProducts
from django.db import transaction
from inventory.models import Stock
from driver.models import vehicletypecategory


@shared_task(bind=True)
def set_pick_up_method(self, order_id):
    truck = vehicletypecategory.objects.filter(vehicle_type="TRUCK").values_list(
        "category", flat=True
    )
    car = vehicletypecategory.objects.filter(vehicle_type="CAR").values_list(
        "category", flat=True
    )

    order = Order.objects.filter(pk=order_id)
    order_categories = order.values_list(
        "order__products__product__category", flat=True
    ).distinct()
    order = order[0]
    bool = False
    for order_category in order_categories:
        if order_category in truck:
            order.pick_up_method = "TRUCK"
            order.save()
            return "set pick up method for order 1"
        elif order_category in car:
            order.pick_up_method = "CAR"
            bool = True
        elif not bool:
            order.pick_up_method = "BIKE"
    order.save()

    return "set pick up method for order 123"


@shared_task(bind=True)
def add_product_bought_from_supplier(self, order):
    order = Order.objects.get(pk=order)
    customer = order.cart.customer
    products = OrderProducts.objects.filter(order=order)
    products = products.values_list("products__product__supplier", "quantity")
    with transaction.atomic():
        for product in products:
            supplier = SupplierProfile.objects.get(pk=product[0])
            p, created = ProductBoughtFromSupplier.objects.get_or_create(
                customer=customer, supplier=supplier
            )
            if not created:
                p.products_bought += product[1]
            else:
                p.products_bought = product[1]
            p.save()

    return "add counts to the table successfully"


@shared_task(bind=True)
def deduct_from_products_stock(self, order_id):
    order = Order.objects.get(pk=order_id)
    products = OrderProducts.objects.filter(order=order)
    with transaction.atomic():
        for product in products:
            stock = Stock.objects.filter(product_detail=product.products).first()
            stock.quantity_in_stock -= product.quantity
            stock.products_sold += product.quantity
            stock.save()
    return "deduct from products is successfull 123"


@shared_task(bind=True)
def return_to_stock(self, order):
    order = Order.objects.get(order=order)
    products = OrderProducts.objects.filter(order=order)
    with transaction.atomic():
        for product in products:
            stock = Stock.objects.filter(product_detail=product.products).first()
            stock.quantity_in_stock += product.quantity
            stock.products_sold -= product.quantity
            stock.save()
