from .views import (
    ProductList,
    ProductDetailDetail,
    CategoryList,
    CategoryDetail,
    ProductTypeList,
    ProductSizeList,
    ProductSizeValueList,
    ProductColorList,
    ProductDetailList,
    ProductTypeDetail,
    ProductDetailView,
)
from django.urls import path

urlpatterns = [
    path("category/", CategoryList.as_view()),
    path("category/<slug:slug>", CategoryDetail.as_view()),
    path("product_type/", ProductTypeList.as_view()),
    path("product_type/<str:name>", ProductTypeDetail.as_view()),
    path("product_size/", ProductSizeList.as_view()),
    path("product_size_value/", ProductSizeValueList.as_view()),
    path("product_color/", ProductColorList.as_view()),
    path("product_add/", ProductList.as_view()),
    path("products/<slug:slug>", ProductDetailView.as_view()),
    path("product/<slug:slug>", ProductDetailList.as_view()),
    path("product_detail/<int:pk>", ProductDetailDetail.as_view()),
]
