from inventory.models import Product, ProductDetail, Stock
from Users.models import CustomerProfile
from .utils import validate_rating
from django.utils import timezone
from django.db import models


class Review(models.Model):
    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=False, default=0, validators=[validate_rating])
    comment = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "review"

    def save(self, *args, **kwargs):
        if self.product:
            self.product.reviews_count += 1
            self.product.average_rating = (
                (
                    (self.product.reviews_count - 1) * self.product.average_rating
                    + self.rating
                )
            ) / self.product.reviews_count
            self.product.save()
        return super().save(*args, **kwargs)


class ReturnReason(models.Model):
    value = models.CharField(max_length=50)

    class Meta:
        db_table = "return_reason"


class ReturnMethod(models.Model):
    return_reason = models.ForeignKey(ReturnReason, on_delete=models.CASCADE)
    return_method = models.CharField(max_length=25)
    fees_applied = models.BooleanField()


class Returnal(models.Model):
    # class ReturnReason(models.TextChoices):
    #     SIZE_ISSUES = "SIZE_ISSUES", "SIZE_ISSUES"
    #     DAMAGED_ITEM = "DAMAGED_ITEM", "DAMAGED_ITEM"
    #     DID_NOT_MEET_EXPECTATIONS = (
    #         "DID_NOT_MEET_EXPECTATIONS",
    #         "DID_NOT_MEET_EXPECTATIONS",
    #     )
    #     CHANGED_MIND = "CHANGED_MIND", "CHANGED_MIND"
    #     INCORRECT_ORDER = "INCORRECT_ORDER", "INCORRECT_ORDER"
    #     MISLEADING_PRODUCT_INFORMATION = (
    #         "MISLEADING_PRODUCT_INFORMATION",
    #         "MISLEADING_PRODUCT_INFORMATION",
    #     )
    #     INCOMPATIABILITY_OR_TECHNICAL_ISSUES = (
    #         "INCOMPATIABILITY_OR_TECHNICAL_ISSUES",
    #         "INCOMPATIABILITY_OR_TECHNICAL_ISSUES",
    #     )
    #     OTHER = "OTHER", "OTHER"

    customer = models.ForeignKey(CustomerProfile, on_delete=models.CASCADE, null=True)
    product_detail = models.ForeignKey(
        ProductDetail, on_delete=models.CASCADE, null=True
    )
    return_reason = models.ForeignKey(ReturnReason, on_delete=models.CASCADE, null=True)
    return_method = models.ForeignKey(ReturnMethod, on_delete=models.CASCADE, null=True)
    comment = models.TextField(null=True)
    is_approved = models.BooleanField(default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)

    class Meta:
        db_table = "returnal"

    def save(self, *args, **kwargs):
        if self.is_approved:
            stock = Stock.objects.get(product_detail=self.product_detail)
            stock.products_sold -= 1
            stock.quantity_in_stock += 1
            stock.save()
        return super().save(*args, **kwargs)


# remember to add choices to user to choose from for the reason of returnal and maybe leave a place to say something !
