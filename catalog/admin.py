from django.contrib import admin
from .models import Product,ProductDetail,Category

admin.site.register(Product)
admin.site.register(ProductDetail)
admin.site.register(Category)