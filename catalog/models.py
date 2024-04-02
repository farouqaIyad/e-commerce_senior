from django.utils import timezone
from django.db import models
from Users.models import User


class Category(models.Model):
    category_name = models.CharField(max_length=255,unique = True)
    class Meta:
        db_table = 'category'

class SubCategory(models.Model):
    sub_category_name = models.CharField(max_length=255,unique = True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    #now i could do category.subcategory.all()
    class Meta:
        db_table = 'subcategory'

class ProductImage(models.Model):
    pass

class Product(models.Model):
    product_name = models.CharField(max_length=255,unique=True) 
    price = models.IntegerField()
    quantity_in_stock = models.IntegerField()
    description = models.TextField()
    date_created = models.DateTimeField(default = timezone.now)
    times_bought = models.IntegerField(default = 0)
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    supplier = models.ForeignKey(User,on_delete = models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory)
    
    #some of the relationships will be with review and supplier and categories and 
    #rating = whatever

    class Meta: 
        db_table = 'product' 
        ordering = ['-date_created'] 

    @property
    def is_best_seller(self):
        #thinking the logic here would be that for each category there will be best sellers 
        #max_bought = 0
        #if self.times_bought == max(Category.Product)
        pass

    @property
    def is_out_of_stock(self):
        if self.quantity_in_stock == 0:
            return True
        return False
    

