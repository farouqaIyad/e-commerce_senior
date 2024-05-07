from catalog.models import Product


def save_products_to_order(order, products):
    for product in products:
        product = Product.objects.get(id=product.id)
        product.times_bought += 1
        product.quantity_in_stock -= 1
        order.product.add(product)
        product.save()
    order.save()
