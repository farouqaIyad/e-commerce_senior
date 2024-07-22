from django.urls import path
from .views import AddressList, AddressDetail, OrderList, OrderDetail, DriverOrderList

urlpatterns = [
    path("address/", AddressList.as_view()),
    path("address/<int:pk>", AddressDetail.as_view()),
    path("order/", OrderList.as_view()),
    path("order/<int:pk>", OrderDetail.as_view()),
    path("order_test/", DriverOrderList.as_view()),
]
