from .views import (
    CategoryList,
    CategoryDetail,
    ProductSizeList,
    ProductSizeValueList,
    ProductSizeValueDetail,
    ProductColorList,
    BrandList,
)
from django.urls import path

urlpatterns = [
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<slug:slug>/", CategoryDetail.as_view(), name="category-detail"),
    path("product-sizes/", ProductSizeList.as_view()),
    path("product-size-values/", ProductSizeValueList.as_view()),
    path("product-size-values/<str:name>/", ProductSizeValueDetail.as_view()),
    path("product-colors/", ProductColorList.as_view(), name="product-color-list"),
    path("brands/<slug:slug>/", BrandList.as_view(), name="brand-list"),
]
