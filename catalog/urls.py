
from django.urls import path
from .views import add_product,CategoryList,CategoryDetail,SubCategoryList,SubCategoryDetail

urlpatterns = [
    path('product/add/', add_product),
    path('product/view/<int:pk>', view_product),
    path('category/', CategoryList.as_view()),
    path('category/<int:pk>', CategoryDetail.as_view()),
    path('subcategory/', SubCategoryList.as_view()),
    path('subcategory/<int:pk>', SubCategoryDetail.as_view()),

    path('subcategory/add/', add_subcategory),    
]