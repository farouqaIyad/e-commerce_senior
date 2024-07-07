from django.urls import path
from .views import SupplierSignupAPIView, SupplierList, SupplierDetail, ApproveSupplier


urlpatterns = [
    path("signup/", SupplierSignupAPIView.as_view()),
    path("view", SupplierList.as_view()),
    path("view/<int:pk>", SupplierDetail.as_view()),
    path("approve/", ApproveSupplier.as_view()),
]
