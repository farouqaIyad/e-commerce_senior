from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Category


@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, **kwargs):
    if not created and not instance.is_active:
        if not instance.is_leaf_node():
            categories = instance.get_children()
            for category in categories:
                category.is_active = instance.is_active
                print("Category updated:", category.name)
                category.save()


@receiver(post_delete, sender=Category)
def category_post_delete(sender, instance, **kwargs):
    if not instance.is_leaf_node():
        categories = instance.get_children()
        categories.delete()
        print("deleted the children categories")


# @receiver(post_save, sender=Product)
# def product_post_save(sender, instance, created, **kwargs):
#     if not created and not instance.is_active:
#         product_details = instance.product_d_set.all()
#         for sub_product in product_details:
#             sub_product.is_active = False
#             sub_product.save()
