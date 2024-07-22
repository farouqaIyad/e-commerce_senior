from celery import shared_task
from .models import ProductBoughtFromSupplier, SupplierProfile, Order, OrderProducts
from django.db import transaction
from catalog.models import Stock
from driver.models import vehicletypecategory


@shared_task(bind = True)
def set_pick_up_method(self,order_id):
    truck = vehicletypecategory.objects.filter(vehicle_type='TRUCK').values_list('category',flat = True)
    car = vehicletypecategory.objects.filter(vehicle_type='CAR').values_list('category',flat = True)

    order = Order.objects.get(pk = order_id)
    order_category = order.values_list("order__products__product__category",flat = True).distinct()
    if order_category in truck:
        order.pick_up_method = "TRUCK"
    elif order_category in car:
        order.pick_up_method = "CAR"
    else:
        order.pick_up_method = 'BIKE'
    order.save()
    return 'set pick up method for order'



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
def deduct_from_products_stock(self, order):
    order = Order.objects.get(order=order)
    products = OrderProducts.objects.filter(order=order)
    with transaction.atomic():
        for product in products:
            stock = Stock.objects.filter(product_detail=product.products).first()
            stock.quantity_in_stock -= product.quantity
            stock.products_sold += product.quantity
            stock.save()


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


