from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    SupplierSignupAPIView,
    CustomerSignupAPIView,
    DriverSignupAPIView,
    UserLoginAPIView,
    delete_account,
)
from django.urls import path

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("supplier/signup/", SupplierSignupAPIView.as_view()),
    path("customer/signup/", CustomerSignupAPIView.as_view()),
    path("driver/signup/", DriverSignupAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("delete/", delete_account),
]
