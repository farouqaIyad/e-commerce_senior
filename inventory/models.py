from django.db import models
from .utils import generate_sku
from catalog.models import Category, Brand, ProductAttribute, ProductColor, Size_Value
from supplier.models import SupplierProfile
from django.db.models import OuterRef, Exists
from django.utils.text import slugify


class ProductManager(models.Manager):

    def with_wishlist_status(self, user):
        from wishlist_cart.models import Wishlist

        return self.get_queryset().annotate(
            in_wishlist=Exists(
                Wishlist.objects.filter(
                    product__product_id=OuterRef("pk"), customer=user.customerprofile
                )
            )
        )


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    description = models.TextField(unique=False, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True, editable=False)
    main_price = models.IntegerField(null=True, blank=True)
    main_sale_price = models.IntegerField(default=0)
    reviews_count = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.00)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    main_image = models.CharField(max_length=255)

    objects = ProductManager()

    def __str__(self):
        return "{}".format(self.id)

    class Meta:
        db_table = "product"
        indexes = [models.Index(fields=["slug"], name="product_slug_idx")]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductDetail(models.Model):
    sku = models.CharField(max_length=20, null=False, blank=True)
    product = models.ForeignKey(
        Product, related_name="product_detail", on_delete=models.CASCADE
    )
    price = models.IntegerField(null=False, blank=False)
    sale_price = models.IntegerField(default=0)
    color = models.ForeignKey(
        ProductColor, null=True, blank=True, on_delete=models.CASCADE
    )
    size = models.ForeignKey(
        Size_Value, null=True, blank=True, on_delete=models.CASCADE
    )
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)
    image_set_id = models.ForeignKey(
        "ProductImageSet", on_delete=models.CASCADE, null=True
    )

    objects = models.Manager()

    class Meta:
        db_table = "product_detail"

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = generate_sku(self.product.name)
        if self.is_main:
            if self.sale_price:
                self.product.main_sale_price = self.sale_price
            self.product.main_price = self.price
            self.product.save()

        return super().save(*args, **kwargs)


class Stock(models.Model):
    product_detail = models.OneToOneField(
        ProductDetail, related_name="stock", on_delete=models.CASCADE
    )
    quantity_in_stock = models.IntegerField(default=0)
    products_sold = models.IntegerField(default=0)

    class Meta:
        db_table = "stock"

    def __str__(self):
        return "{}".format(self.quantity_in_stock)


class ProductImageSet(models.Model):
    image_set_name = models.CharField(max_length=255, unique=True)


class ProductImage(models.Model):
    image_set_id = models.ForeignKey(ProductImageSet, on_delete=models.CASCADE)
    image_url = models.ImageField(
        unique=False, upload_to="products", default="products/default.png"
    )


class ProductAttributeValues(models.Model):
    product_attr = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="attrs")
    value = models.CharField(max_length=255)

    class Meta:
        db_table = "product_attribute_values"


## materiliazed views

class ProductAttrsMaterializedViews(models.Model):
    id = models.CharField(db_column='id',primary_key=True)
    attribute_name = models.CharField(db_column='attribute_name',max_length=255)
    attribute_value = models.CharField(db_column='attribute_value',max_length=255)
    product_id = models.IntegerField(db_column='product_id')
    class Meta:
        db_table = 'attrss'
        managed = False

class ImagesMaterializedView(models.Model):
    id = models.IntegerField(db_column="id", primary_key=True)
    image_set = models.IntegerField(db_column="image_set")
    product_id = models.IntegerField(db_column="product_id")
    image_url = models.CharField(db_column="image_url", max_length=255)

    class Meta:
        db_table = "images"
        managed = False
