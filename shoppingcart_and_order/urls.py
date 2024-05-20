from django.urls import path
from .views import ShoppingCartList, OrderList, ShoppingCartDetail

urlpatterns = [
    path("shoppingcart/", ShoppingCartList.as_view()),
    path("shoppingcart/<int:pk>", ShoppingCartDetail.as_view()),
    path("order/", OrderList.as_view()),
]
