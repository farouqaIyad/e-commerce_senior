
from .views import ProductList,ProductDetail,CategoryList,CategoryDetail,SubCategoryList,SubCategoryDetail
from django.urls import path

urlpatterns = [
    path('product/', ProductList.as_view()),
    path('product/<int:pk>', ProductDetail.as_view()),
    path('category/', CategoryList.as_view()),
    path('category/<int:pk>', CategoryDetail.as_view()),
    path('subcategory/', SubCategoryList.as_view()),
    path('subcategory/<int:pk>', SubCategoryDetail.as_view()),
]