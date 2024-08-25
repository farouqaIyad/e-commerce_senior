from django.urls import path

from .views import (
    ProductList,
    ProductDetailDetail,
    ProductDetailList,
    ProductDetailView,
    StartUpList,
    SupplierPageList,
    StockList,
    StockDetail,
    FilterParams,
)


urlpatterns = [
    path("products/", ProductList.as_view()),
    path("products/<slug:slug>/", ProductDetailView.as_view()),
    path("products/<slug:slug>/details/", ProductDetailList.as_view()),
    path("product-details/<int:pk>/", ProductDetailDetail.as_view()),
    path("products/<slug:slug>/stock/", StockList.as_view()),
    path("product-stock/<int:pk>/", StockDetail.as_view()),
    path("startup/", StartUpList.as_view()),
    path("supplier/products/", SupplierPageList.as_view()),
    path("filter/params/", FilterParams.as_view()),
]
