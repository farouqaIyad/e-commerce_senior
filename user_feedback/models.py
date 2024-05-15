from catalog.models import Product
from django.utils import timezone
from Users.models import User
from django.db import models
from .utils import validate_rating


class Review(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    rating = models.IntegerField(blank=False, default=0, validators=[validate_rating])
    comment = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "review"

    def save(self, *args, **kwargs):
        if self.product:
            self.product.reviews_count += 1
            print("found")
            self.product.average_rating += self.rating / self.product.reviews_count
            self.product.save()
        return super().save(*args, **kwargs)


class Complaints(models.Model):
    # order = models.OneToOneField(Order,on_delete = models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # complain_type = will do this one later
    # status_type also done later
    date_created = models.DateTimeField(default=timezone.now)

    class Meta:
        db_table = "complaints"
