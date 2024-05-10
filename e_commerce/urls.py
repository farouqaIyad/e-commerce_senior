from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("Users/", include("Users.urls")),
    path("catalog/", include("catalog.urls")),
    path("user_feedback/", include("user_feedback.urls")),
    path("", include("shoppingcart_and_order.urls")),
    path("", include("address.urls")),
    path("", include("wishlist.urls")),
    path("", include("search_and_filter.urls")),
]
