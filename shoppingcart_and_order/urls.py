from django.urls import path
from .views import (
    ShoppingCartList,
    OrderList,
    ShoppingCartDetail,
    WishlistConvertToShoppingCart,
)

urlpatterns = [
    path("shoppingcart/", ShoppingCartList.as_view()),
    path("shoppingcart/<int:pk>", ShoppingCartDetail.as_view()),
    path("wishlist_to_shoppingcart/", WishlistConvertToShoppingCart.as_view()),
    path("order/", OrderList.as_view()),
]
