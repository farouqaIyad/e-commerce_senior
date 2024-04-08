

@receiver(post_save, sender=User)
def create_shopping_cart(sender, instance, created, **kwargs):
    if created:  # Only create a cart for new users
        ShoppingCart.objects.create(customer=instance)