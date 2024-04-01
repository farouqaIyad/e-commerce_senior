
from django.urls import path
from .views import add_product,add_category,add_subcategory,view_product

urlpatterns = [
    path('product/add/', add_product),
    path('product/view/<int:pk>', view_product),
    path('category/add/', add_category),
    path('subcategory/add/', add_subcategory),    
]