from django.urls import path
from .views import AddressList, AddressDetail, OrderList, OrderDetail, DriverOrderList,DriverOrderDetail,DriverFlagPickedUp,order_test,MyOrders,DriverFlagDelivered

urlpatterns = [
    path("address/", AddressList.as_view()),
    path("address/<int:pk>", AddressDetail.as_view()),
    path("order/", OrderList.as_view()),
    path("order/<int:pk>", OrderDetail.as_view()),
    path("driver_order/", DriverOrderList.as_view()),
    path("driver_order/<int:pk>", DriverOrderDetail.as_view()),
    path("order_accept/<int:pk>", DriverFlagPickedUp.as_view()),
    path("order_deliver/<int:pk>", DriverFlagDelivered.as_view()),
    path("order_test/", order_test.as_view()),
    path("my_order/",MyOrders.as_view())

]
