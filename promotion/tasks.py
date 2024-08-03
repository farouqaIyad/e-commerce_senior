from catalog.models import ProductDetail
from django.db import transaction
from celery import shared_task
from datetime import datetime
from decimal import Decimal
from math import ceil
from .models import Promotion, Coupon, SupplierProfile
from notifications.tasks import (
    promo_notify_customers,
    notify_customers_deserving_coupon,
)


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


@shared_task(bind=True)
def start_promotion(self, promotion_id):
    with transaction.atomic():
        promotion = Promotion.objects.get(pk=promotion_id)
        reduction = promotion.discount_percentege / 100
        products_detail = ProductDetail.objects.filter(
            product__products_on_promotion__promotion=promotion
        )
        for product_detail in products_detail:
            product_detail.sale_price = ceil(
                product_detail.price - (product_detail.price * Decimal(reduction))
            )
            product_detail.save()
        promo_notify_customers.delay(promotion.id)

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


@shared_task(bind=True)
def coupon_management(self):
    with transaction.atomic():
        coupons = Coupon.objects.all()
        now = datetime.now().date()
        for coupon in coupons:
            print(coupon)
            if coupon.time_end < now:
                coupon.is_active = False
            else:
                if coupon.time_start <= now:
                    coupon.is_active = True

                else:
                    coupon.is_active = False
            coupon.save()
        if coupon.is_active:
            give_coupons.delay()
    return "coupons managed "


@shared_task(bind=True)
def give_coupons(self):
    from order.models import CustomerProfile

    suppliers = SupplierProfile.objects.filter(coupon__is_active=True)
    for supplier in suppliers:
        products_to_earn_coupon = supplier.coupon.products_to_earn
        users = CustomerProfile.objects.filter(
            cus__supplier=supplier, cus__products_bought__gte=products_to_earn_coupon
        ).values_list("user__id", flat=True)
        if users:
            notify_customers_deserving_coupon.delay(list(users), supplier.coupon.pk)
    return "coupons given"
