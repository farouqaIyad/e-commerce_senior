from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .utils import generate_sku
from Users.models import User, SupplierProfile
from django.db import models


class CategoryManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super(CategoryManager, self).get_queryset().filter(is_active=True)


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        unique=False,
    )
    image_url = models.ImageField(
        unique=False,
        upload_to="images/category/",
        default="images/category/default.png",
    )

    active_categories = CategoryManager()
    objects = models.Manager()

    class MPTTMeta:
        order_insertion_by = ["name"]

    class Meta:
        db_table = "category"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    product_size = models.ForeignKey("ProductSize", on_delete=models.CASCADE, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_type"


class ProductSize(models.Model):

    product_size = models.CharField(max_length=50)

    class Meta:
        db_table = "product_size"


class Size_Value(models.Model):
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "size_values"
        unique_together = ("size", "value")


class ProductColor(models.Model):

    color = models.CharField(max_length=20)

    class Meta:
        db_table = "colors"


class ProductManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super(ProductManager, self).get_queryset().filter(is_active=True)


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    description = models.TextField(unique=False, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.ForeignKey(
        ProductType, related_name="product_type", on_delete=models.CASCADE
    )

    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)
    main_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        unique=False,
        null=True,
        blank=True,
    )
    main_sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, unique=False, null=True, blank=True
    )
    reviews_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0)
    attributes = models.ManyToManyField(
        "ProductTypeAttributes", through="ProductTypeAttributesValues"
    )

    main_image = models.CharField(unique=False, max_length=255)

    active_products = ProductManager()
    objects = models.Manager()

    class Meta:
        db_table = "product"
        ordering = ["-date_created"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductDetailManager(models.Manager):
    def get_queryset(self) -> models.QuerySet:
        return super(ProductDetailManager, self).get_queryset().filter(is_active=True)


class ProductDetail(models.Model):
    sku = models.CharField(max_length=20, unique=True, null=False, blank=True)
    product = models.ForeignKey(
        Product, related_name="product_detail", on_delete=models.CASCADE
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0.01,
        unique=False,
        null=False,
        blank=False,
    )
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    color = models.ManyToManyField(ProductColor)
    size = models.ManyToManyField(Size_Value)
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)
    active_product_details = ProductDetailManager()
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


class ProductAttribute(models.Model):
    attribute = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "product_attribute"


class ProductTypeAttributes(models.Model):
    attribute = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_type_attributes"


class ProductTypeAttributesValues(models.Model):
    type_attr = models.ForeignKey(ProductTypeAttributes, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(unique=True, max_length=255)

    class Meta:
        db_table = "product_type_attr_value"


# class ProductImage(models.Model):
#     product = models.ForeignKey(
#         Product, related_name="images", on_delete=models.CASCADE
#     )
#     is_main = models.BooleanField(default=False)
#     image_url = models.ImageField(
#         unique=False, upload_to="images/", default="images/default.png"
#     )

#     def save(self, *args, **kwargs):
#         if self.is_main:
#             self.product.main_image = self.image_url
#             self.product.save()
#         return super().save(*args, **kwargs)
