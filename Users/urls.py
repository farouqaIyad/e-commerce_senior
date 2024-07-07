from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CustomerSignupAPIView,
    DriverSignupAPIView,
    UserLoginAPIView,
    delete_account,
    CustomerList,
    CustomerDetail,
)
from django.urls import path

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("customer/signup/", CustomerSignupAPIView.as_view()),
    path("driver/signup/", DriverSignupAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("delete/", delete_account),
    path("admin/customers", CustomerList.as_view()),
    path("admin/customers/<int:pk>", CustomerDetail.as_view()),
]
