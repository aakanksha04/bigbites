from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=254, null=True)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=5, decimal_places=2)
    available = models.BooleanField(default=False, null=True, blank=False)
    img = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name    
        
    @property
    def imageURL(self):
        try:
            url = self.img.url
        except:
            url = ''
        return url

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False)
    transaction_id = models.CharField(max_length=200, null=True)
    product = models.ManyToManyField('OrderItem', related_name='menu', blank=True)
    # order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return str(self.id)

    # @property
    # def shipping(self):
    #     available = False
    #     orderitems = self.orderitem_set.all()
    #     for i in orderitems:
    #         if i.product.available == False:
    #             available = True
    #     return available

    @property
    def get_cart_total(self):
        orderitems  = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property
    def get_cart_items(self):
        orderitems  = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingTo(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    roll_no = models.CharField(max_length=10, null=True)
    date_added = models.DateTimeField(auto_now_add=True)


# -----------------------------------------------------------------------------------------------
# class MenuItem(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     image = models.ImageField(upload_to='menu_images/')
#     price = models.DecimalField(max_digits=5, decimal_places=2)
#     category = models.ManyToManyField('Category', related_name='item')

#     def __str__(self):
#         return self.name


# class Category(models.Model):
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.name


class OrderModel(models.Model):
    created_on = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    items = models.ManyToManyField('Product', related_name='menu', blank=True)
    name = models.CharField(max_length=50, blank=True)
    # email = models.CharField(max_length=50, blank=True)
    # street = models.CharField(max_length=50, blank=True)
    # city = models.CharField(max_length=50, blank=True)
    # state = models.CharField(max_length=15, blank=True)
    # zip_code = models.IntegerField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    is_shipped = models.BooleanField(default=False)

    def __str__(self):
        return f'Order: {self.created_on.strftime("%b %d %I: %M %p")}'
