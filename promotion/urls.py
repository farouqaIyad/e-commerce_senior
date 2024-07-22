from django.urls import path
from .views import (
    CouponList,
    CouponDetail,
    UseCoupon,
    PromotionList,
    ProductOnPromotionList,
    PromotionDetail,
)

urlpatterns = [
    path("coupon/", CouponList.as_view()),
    path("coupon/<int:pk>", CouponDetail.as_view()),
    path("use_coupon/", UseCoupon.as_view()),
    path("promotion/", PromotionList.as_view()),
    path("promotion/<int:pk>", PromotionDetail.as_view()),
    path("promotion/products/<int:pk>", ProductOnPromotionList.as_view()),
]
