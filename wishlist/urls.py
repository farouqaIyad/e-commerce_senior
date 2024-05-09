from .views import (
    WishlistList,
    WishlistDetail
)
from django.urls import path

urlpatterns = [
    path("wishlist/", WishlistList.as_view()),
    path("wishlist/<int:pk>", WishlistDetail.as_view()),

]
