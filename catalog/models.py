from django.utils.translation import gettext_lazy as _
from mptt.models import MPTTModel, TreeForeignKey
from django.utils.text import slugify
from django.db import models


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


class ProductAttribute(models.Model):
    name = models.CharField(max_length=255, unique=True)

    class Meta:
        db_table = "product_attribute"


class ProductCategoryAttributes(models.Model):
    category_id = models.ForeignKey(Category, on_delete=models.CASCADE)
    attr_id = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE)

    class Meta:
        db_table = "product_category_attributes"
