from .views import AddressList,AddressDetail
from django.urls import path


urlpatterns = [
    path('address/', AddressList.as_view()),
    path('address/<int:pk>', AddressDetail.as_view())
]