from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    CustomerSignupAPIView,
    UserLoginAPIView,
    AdminCustomersList,
    CustomerDetail,
    UserLogoutAPIView,
)
from rest_framework.authtoken.views import obtain_auth_token
from django.urls import path

urlpatterns = [
    path("token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("customer/signup/", CustomerSignupAPIView.as_view()),
    path("login/", UserLoginAPIView.as_view()),
    path("logout/", UserLogoutAPIView.as_view()),
    path("admin/customers", AdminCustomersList.as_view()),
    path("customer/", CustomerDetail.as_view()),
]


from rest_framework_simplejwt.models import TokenUser
