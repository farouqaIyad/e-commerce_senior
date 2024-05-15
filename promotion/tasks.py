from celery import shared_task
from datetime import datetime
from decimal import Decimal
from math import ceil
from django.db import transaction
from .models import Promotion,ProductOnPromotion,ProductDetail,Product

@shared_task(bind= True)
def promotion_prices(reduction_amount, obj_id):
    with transaction.atomic():
        reduction = reduction_amount / 100
        products = Product.active_products.filter(productonpromotion__promotion_id = obj_id)
        for product in products:
            products_details = ProductDetail.active_product_details.filter(product = product)
            for product_detail in products_details:
                product_detail.sale_price = ceil(product_detail.price - (product_detail.price * Decimal(reduction)))
                product.save()
                print("reached here")
    return "done"