from django.db import models
from Users.models import User
from catalog.models import Product
from django.utils import timezone

class Review(models.Model):
    customer = models.ForeignKey(User,on_delete = models.CASCADE)
    product = models.ForeignKey(Product,on_delete = models.CASCADE)
    rating = models.IntegerField()
    comment = models.TextField()
    date_created = models.DateTimeField(default = timezone.now)

    class Meta:
        db_table = 'review'


class Complaints(models.Model):
    #order = models.OneToOneField(Order,on_delete = models.CASCADE)
    user = models.ForeignKey(User,on_delete = models.CASCADE)
    #complain_type = will do this one later
    #status_type also done later
    date_created = models.DateTimeField(default = timezone.now)
    class Meta:
        db_table = 'complaints'
