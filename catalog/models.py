from mptt.models import MPTTModel, TreeForeignKey, TreeManyToManyField
from django.utils.translation import gettext_lazy as _
from django.utils.text import slugify
from .utils import generate_sku
from Users.models import User
from django.db import models


class Category(MPTTModel):
    name = models.CharField(max_length=100, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    description = models.TextField()
    is_active = models.BooleanField(default=True)
    parent = TreeForeignKey(
        "self",
        on_delete=models.CASCADE,
        related_name="children",
        null=True,
        blank=True,
        unique=False,
    )

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
    product_size = models.ForeignKey("ProductSize", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_type"


class ProductSize(models.Model):
    class Size(models.TextChoices):
        CLOTHES_SIZE = "CLOTHES_SIZE", "Clothes_size"
        SHOES_SIZE = "SHOES_SIZE", "Shoes_size"
        TV_SIZE = "TV_SIZE", "Tv_size"
        STORAGE_SIZE = "STORAGE_SIZE", "Storage_size"
        BED_SIZE = "BED_SIZE", "Bed_size"

    product_size = models.CharField(max_length=50, choices=Size.choices)

    class Meta:
        db_table = "product_size"


class Size_Value(models.Model):
    size = models.ForeignKey(ProductSize, on_delete=models.CASCADE)
    value = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "size_values"
        unique_together = ("size", "value")


class ProductColor(models.Model):
    class Colors(models.TextChoices):
        RED = "RED", "Red"
        BLUE = "BLUE", "Blue"
        GREEN = "GREEN", "Green"
        YELLOW = "YELLOW", "Yellow"
        ORANGE = "ORANGE", "Orange"
        PURPLE = "PURPLE", "Purple"
        PINK = "PINK", "Pink"
        WHITE = "WHITE", "White"
        BLACK = "BLACK", "Black"
        GRAY = "GRAY", "Gray"
        BROWN = "BROWN", "Brown"

    color = models.CharField(max_length=20, choices=Colors.choices)

    class Meta:
        db_table = "colors"


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True, null=False, blank=False)
    slug = models.SlugField(max_length=150, unique=True, null=False, blank=False)
    price = models.DecimalField(
        max_digits=10, decimal_places=2, unique=False, null=False, blank=False
    )
    sale_price = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True
    )
    description = models.TextField(unique=False, null=False, blank=False)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    product_type = models.ForeignKey(
        ProductType, related_name="product_type", on_delete=models.CASCADE
    )

    supplier = models.ForeignKey(User, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True, editable=False)

    class Meta:
        db_table = "product"
        ordering = ["-date_created"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)


class ProductDetail(models.Model):
    sku = models.CharField(max_length=20, unique=True, null=False, blank=True)
    product = models.ForeignKey(
        Product, related_name="product", on_delete=models.CASCADE
    )
    color = models.ManyToManyField(ProductColor)
    size = models.ManyToManyField(Size_Value)
    is_active = models.BooleanField(default=True)
    is_main = models.BooleanField(default=False)

    class Meta:
        db_table = "product_detail"

    def save(self, *args, **kwargs):
        if not self.sku:
            self.sku = generate_sku(self.product.name)
        return super().save(*args, **kwargs)


class Stock(models.Model):
    product_detail = models.OneToOneField(ProductDetail, on_delete=models.CASCADE)
    quantity_in_stock = models.IntegerField(default=0)
    products_sold = models.IntegerField(default=0)

    class Meta:
        db_table = "stock"


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    image_url = models.ImageField(
        unique=False, upload_to="images/", default="images/default.png"
    )
    is_main = models.BooleanField(default=False)

    class Meta:
        db_table = "product_image"
