from django.urls import path
from .views import ShoppingCartList,OrderList

urlpatterns = [
    
    path('shoppingcart/', ShoppingCartList.as_view()),
    path('order/', OrderList.as_view()),
    
]