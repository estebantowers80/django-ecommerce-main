from django.db import models
from django.contrib.auth.models import User

# Create your models here.

# Models Doc: https://docs.djangoproject.com/en/4.1/topics/db/models/
# Model Field Types Doc: https://docs.djangoproject.com/en/4.1/ref/models/fields/#model-field-types
# Model Field Options Doc: https://docs.djangoproject.com/en/4.1/ref/models/fields/

# Cómo definir relaciones: https://betterprogramming.pub/how-to-design-relationships-between-your-django-models-caa01bc17a5c
# Model Relationship examples: https://docs.djangoproject.com/en/4.1/topics/db/examples/

class Category(models.Model):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=255, unique=True)

    # Meta Options Doc: https://docs.djangoproject.com/en/4.1/ref/models/options/#model-meta-options
    class Meta:
        db_table = 'categories'
        verbose_name_plural = 'categories'        

    def __str__(self):
        return self.name

# ON_DELETE Options Doc:
# https://docs.djangoproject.com/en/4.1/ref/models/fields/#django.db.models.ForeignKey.on_delete
# https://stackoverflow.com/questions/38388423/what-does-on-delete-do-on-django-models

class Product(models.Model):    
    category = models.ManyToManyField(Category, related_name="products")
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='images/')
    slug = models.SlugField(max_length=255, unique=True)
    price = models.DecimalField(max_digits=9, decimal_places=2)
    is_active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
    #count_sold = models.IntegerField(default=0, verbose_name=_('count sold'))

    class Meta:
        db_table = 'products'
        verbose_name_plural = 'products'
        ordering = ['-created']

    def __str__(self):
        return self.name

    


class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    identification = models.CharField(max_length=13, default='', unique=True)
    full_name = models.CharField(max_length=75)
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=10)

    class Meta:
        db_table = 'customers'
        verbose_name_plural = 'customers'

    def __str__(self):
        return self.full_name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    complete = models.BooleanField(default=False)
    total = models.DecimalField(max_digits=9, decimal_places=2)    
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)	

    class Meta:
        db_table = 'orders'
        verbose_name_plural = 'orders'
        ordering = ["-created"]

    def __str__(self):
        return str(self.id)
	
    @property
    def get_cart_total(self):
        order_items = self.order_items.all()
        total = sum([item.get_subtotal for item in order_items])
        return total 

    @property
    def get_cart_items(self):
        order_items = self.order_items.all()
        total = sum([item.quantity for item in order_items])
        return total   


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="order_items", on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'order_items'
        verbose_name_plural = 'order_items'

    def __str__(self):
        return str(self.id)
	
    @property
    def get_subtotal(self):
        subtotal = self.product.price * self.quantity
        return subtotal



class ShippingAddress(models.Model):    
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    city = models.CharField(max_length=200)	
    address = models.CharField(max_length=200)
    phone = models.CharField(max_length=10)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'shipping_addresses'
        verbose_name_plural = 'shipping_addresses'

    def __str__(self):
        return self.address