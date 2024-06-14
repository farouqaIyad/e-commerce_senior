from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path("admin/", admin.site.urls),
    path("Users/", include("Users.urls")),
    path("catalog/", include("catalog.urls")),
    path("user_feedback/", include("user_feedback.urls")),
    path("", include("shoppingcart_and_order.urls")),
    path("", include("address.urls")),
    path("", include("wishlist.urls")),
    path("", include("search_and_filter.urls")),
    path("", include("promotion.urls")),
    path("", include("driver.urls")),
    path("chat", include("chat.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
]
