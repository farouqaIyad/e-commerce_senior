from django.utils.translation import gettext_lazy as _
from pgvector.django import VectorField, HnswIndex
from mptt.models import MPTTModel, TreeForeignKey
from Users.models import User
from django.utils.text import slugify
from .utils import generate_sku
from django.db import models
from supplier.models import SupplierProfile
from sentence_transformers import SentenceTransformer
from django.db.models import OuterRef, Exists


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
    image_url = models.CharField(max_length=255)

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
    attributes = models.ManyToManyField(
        "ProductAttribute", through="ProductTypeAttributes"
    )
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

    def __str__(self):
        return "{}".format(self.value)


class ProductColor(models.Model):

    color = models.CharField(max_length=20)

    class Meta:
        db_table = "colors"

    def __str__(self):
        return "{}".format(self.color)


class Brand(models.Model):
    name = models.CharField(max_length=25, unique=True)
    category = models.ManyToManyField(Category, blank=True, through="CategoriesBrand")

    class Meta:
        db_table = "brand"


class CategoriesBrand(models.Model):
    brand = models.ForeignKey(Brand, related_name="brand", on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


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
    product_type = models.ForeignKey(
        ProductType, related_name="product_type", on_delete=models.CASCADE
    )

    supplier = models.ForeignKey(SupplierProfile, on_delete=models.CASCADE)
    is_active = models.BooleanField(default=True)
    date_created = models.DateField(auto_now_add=True, editable=False)
    main_price = models.IntegerField(null=True, blank=True)
    main_sale_price = models.IntegerField(default=0)
    reviews_count = models.IntegerField(default=0)
    average_rating = models.DecimalField(max_digits=3, decimal_places=2,default=0.00)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, null=True)
    main_image = models.CharField(max_length=255)

    embedding = VectorField(dimensions=384, null=True, blank=True)

    objects = ProductManager()

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        db_table = "product"
        ordering = ["-date_created"]
        indexes = [
            HnswIndex(
                name="product_embedding_hnsw_index",
                fields=["embedding"],
                m=16,
                ef_construction=64,
                opclasses=["vector_cosine_ops"],
            )
        ]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
            model = SentenceTransformer("all-MiniLM-L6-v2")
            self.embedding = model.encode(self.name)
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


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name="images", on_delete=models.CASCADE
    )
    is_main = models.BooleanField(default=False)
    image_url = models.ImageField(
        unique=False, upload_to="products", default="products/default.png"
    )

    def save(self, *args, **kwargs):
        if self.is_main:
            self.product.main_image = (
                "https://donkey-casual-python.ngrok-free.app/media/products/"
                + str(self.image_url)
            )
            self.product.save()
        return super().save(*args, **kwargs)


class ProductAttribute(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "product_attribute"


class ProductTypeAttributes(models.Model):
    type_attr = models.ForeignKey(ProductType, on_delete=models.CASCADE)
    attr = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_type_attributes"


class ProductAttributeValues(models.Model):
    product_attr = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = "product_attribute_values"
