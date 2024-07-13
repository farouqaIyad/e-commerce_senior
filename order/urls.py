from django.urls import path
from .views import (
    AddressList,
    AddressDetail,
    OrderList,
)

urlpatterns = [
    path("address/", AddressList.as_view()),
    path("address/<int:pk>", AddressDetail.as_view()),
    path("order/", OrderList.as_view()),
]
