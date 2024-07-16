from .views import (
    WishlistList,
    ShoppingCartList,
    ShoppingCartDetail,
    WishlistConvertToShoppingCart,
    Test
)
from django.urls import path

urlpatterns = [
    path("wishlist/", WishlistList.as_view()),
    path("shoppingcart/", ShoppingCartList.as_view()),
    path("shoppingcart/<int:pk>", ShoppingCartDetail.as_view()),
    path("wishlist_to_shoppingcart/", WishlistConvertToShoppingCart.as_view()),
    path("test/", Test.as_view()),

]
