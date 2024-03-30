from django.utils import timezone
from django.db import models
from Users.models import User

class Category(models.Model):
    name = models.CharField(max_length=255, unique=True),
    class Meta:
        db_table = 'category'

class SubCategory(models.Model):
    name = models.CharField(max_length=255, unique=True),
    slug = models.SlugField(max_length=255, unique=True)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    #now i could do category.subcategory.all()
    class Meta:
        db_table = 'subcategory'


class Product(models.Model):
    name = models.CharField(max_length=255, unique=True) 
    slug = models.SlugField(max_length=255, unique=True,  
    help_text='Unique value for product page URL, created from name.') 
    price = models.DecimalField(max_digits=9,decimal_places=0)
    quantity_in_stock = models.IntegerField()
    description = models.TextField()
    date_created = models.DateTimeField(default = timezone.now)
    times_bought = models.IntegerField()
    category = models.ForeignKey(Category,on_delete = models.CASCADE)
    sub_category = models.ManyToManyField(SubCategory)
    supplier = models.ForeignKey(User,on_delete = models.CASCADE)
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
    

