from .views import (
    ProductList,
    ProductDetailDetail,
    CategoryList,
    CategoryDetail,
    ProductTypeList,
    ProductSizeList,
    ProductSizeValueList,
    ProductSizeValueDetail,
    ProductColorList,
    ProductDetailList,
    ProductTypeDetail,
    ProductDetailView,
    StartUpList,
    SupplierPageList,
    StockList,
    StockDetail,
    FilterParams,
    BrandList,
)
from django.urls import path

urlpatterns = [
    path("categories/", CategoryList.as_view(), name="category-list"),
    path("categories/<slug:slug>/", CategoryDetail.as_view(), name="category-detail"),
    path("product-types/", ProductTypeList.as_view(), name="product-type-list"),
    path("product-types/<slug:slug>/", ProductTypeDetail.as_view(), name="product-type-detail"),
    path("product-sizes/", ProductSizeList.as_view(), name="product-size-list"),
    path("product-size-values/", ProductSizeValueList.as_view(), name="product-size-value-list"),
    path("product-size-values/<str:name>/", ProductSizeValueDetail.as_view(), name="product-size-value-detail"),
    path("product-colors/", ProductColorList.as_view(), name="product-color-list"),
    path("products/", ProductList.as_view(), name="product-list"),
    path("products/<slug:slug>/", ProductDetailView.as_view(), name="product-detail-view"),
    path("products/<slug:slug>/details/", ProductDetailList.as_view(), name="product-detail-list"),
    path("product-details/<int:pk>/", ProductDetailDetail.as_view(), name="product-detail-detail"),
    path("products/<slug:slug>/stock/", StockList.as_view(), name="stock-list"),
    path("product-stock/<int:pk>/", StockDetail.as_view(), name="stock-detail"),
    path("startup/", StartUpList.as_view(), name="startup-list"),
    path("supplier/products/", SupplierPageList.as_view(), name="supplier-product-list"),
    path("filter/params/", FilterParams.as_view(), name="filter-params"),
    path("brands/<slug:slug>/", BrandList.as_view(), name="brand-list"),
]
