from django.contrib import admin
from django.urls import path, include
import debug_toolbar
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path("admin/", admin.site.urls),
    path("Users/", include("Users.urls")),
    path("catalog/", include("catalog.urls")),
    path("user_feedback/", include("user_feedback.urls")),
    path("", include("order.urls")),
    path("", include("wishlist_cart.urls")),
    path("", include("search_and_filter.urls")),
    path("", include("promotion.urls")),
    path("driver/", include("driver.urls")),
    path("supplier/", include("supplier.urls")),
    path("", include("notifications.urls")),
    path("__debug__/", include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
