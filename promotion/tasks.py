from celery import shared_task
from datetime import datetime
from decimal import Decimal
from math import ceil
from django.db import transaction
from catalog.models import ProductDetail, Product
from rest_framework.response import Response


@shared_task(bind=True)
def promotion_prices(self, discount, product_pk):
    reduction = discount / 100
    products_detail = ProductDetail.active_product_details.filter(product=product_pk)
    for product_detail in products_detail:
        product_detail.sale_price = ceil(
            product_detail.price - (product_detail.price * Decimal(reduction))
        )
        product_detail.save()
