from django.dispatch import receiver
from django.db.models.signals import post_save, post_delete
from .models import Category, Product

# remember to add signals for deleteing the users and their stock
# their wishlist their shopping cart and orders
# for a supplier their products


@receiver(post_save, sender=Category)
def category_post_save(sender, instance, created, **kwargs):
    if not created and not instance.is_active:
        if not instance.is_leaf_node():
            children = instance.get_children()
            for category in children:
                category.is_active = instance.is_active
                print("Category updated:", category.name)
                category.save()  # Save the updated category


@receiver(post_save, sender=Product)
def product_post_save(sender, instance, created, **kwargs):
    if not created and not instance.is_active:
        product_details = instance.product_detail_set.all()
        for sub_product in product_details:
            sub_product.is_active = False
            sub_product.save()
