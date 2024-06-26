from catalog.models import ProductDetail, Product
from rest_framework.response import Response
from django.db import transaction
from celery import shared_task
from datetime import datetime
from decimal import Decimal
from math import ceil
from .models import Promotion


@shared_task(bind=True)
def promotion_management(self):
    with transaction.atomic():
        promotions = Promotion.objects.filter(is_scheduled=True)
        now = datetime.now().date()
        for promotion in promotions:
            if promotion.time_end < now:
                promotion.is_active = False
                end_promotion.delay(promotion.id)
            else:
                if promotion.time_start <= now:

                    promotion.is_active = True
                    start_promotion.delay(promotion.id)
                else:
                    promotion.is_active = False
            promotion.save()
            print(promotion)


@shared_task(bind=True)
def start_promotion(self, promotion_id):
    with transaction.atomic():
        promotion = Promotion.objects.get(pk=promotion_id)
        reduction = promotion.discount_percentege / 100
        products_detail = ProductDetail.active_product_details.filter(
            product__products_on_promotion__promotion=promotion
        )
        for product_detail in products_detail:
            product_detail.sale_price = ceil(
                product_detail.price - (product_detail.price * Decimal(reduction))
            )
            product_detail.save()
    return "promotion applied to all products details"


@shared_task(bind=True)
def end_promotion(self, promotion_id):
    with transaction.atomic():
        promotion = Promotion.objects.get(pk=promotion_id)
        products_detail = ProductDetail.objects.filter(
            product__products_on_promotion__promotion=promotion
        )
        for product_detail in products_detail:
            product_detail.sale_price = None
            product_detail.save()
    return "sale is over"
