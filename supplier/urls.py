from django.urls import path
from .views import (
    SupplierSignupAPIView,
    SupplierList,
    SupplierDetail,
    ApproveSupplier,
    AdminViewSupplier,
)


urlpatterns = [
    path("signup/", SupplierSignupAPIView.as_view()),
    path("view", SupplierList.as_view()),
    path("view_details/", SupplierDetail.as_view()),
    path("approve/", ApproveSupplier.as_view()),
    path("all", AdminViewSupplier.as_view()),
]
