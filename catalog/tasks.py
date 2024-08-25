from celery import shared_task
from datetime import datetime
from decimal import Decimal
from math import ceil
from django.db import transaction
from inventory.models import ProductDetail, ProductColor, Size_Value, Stock, Product

from rest_framework.response import Response
from rest_framework import status
import ast


@shared_task(bind=True)
def save_product_details(
    self, product, quantity_in_stock, prices, colors_ids, sizes_ids
):
    Bool_value = True
    product_details = []
    product = Product.objects.get(pk=product)

    for i in range(len(quantity_in_stock)):

        product_detail = ProductDetail.objects.create(
            product=product, is_main=Bool_value, price=Decimal(prices[i])
        )

        color_id = colors_ids[i] if i < len(colors_ids) else None
        size_id = sizes_ids[i] if i < len(sizes_ids) else None

        if color_id:
            try:
                color = ProductColor.objects.get(id=color_id)
                product_detail.color = color
            except ProductColor.DoesNotExist:
                return "not found"
        if size_id:
            try:
                size = Size_Value.objects.get(id=size_id)
                product_detail.size = size
            except Size_Value.DoesNotExist:
                return "not found"

        product_details.append(product_detail)
        product_detail.save()
        Bool_value = False

    stocks = [
        Stock(product_detail=detail, quantity_in_stock=qis)
        for detail, qis in zip(product_details, quantity_in_stock)
    ]
    Stock.objects.bulk_create(stocks)
    return "product details created"
