from django.contrib import admin
from django.urls import path,include

urlpatterns = [
    path("admin/", admin.site.urls),
    path('Users/', include('Users.urls')),
    path('catalog/', include('catalog.urls')),
    path('user_feedback/', include('user_feedback.urls')),


]
