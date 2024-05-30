from django.db import models
from accounts.models import Customer, Address
from products.models import Product

# Create your models here.
class Order(models.Model):
    
    class Meta:
        verbose_name, verbose_name_plural = 'order', 'orders'
        ordering = ('-created_at',)
        indexes = [
            models.Index(fields=['-created_at'])
        ]

    STATUSES = {
        'P': "Paid",
        'U' : "Unpaid",
        'C' : "Canceled"
    }

    status = models.CharField(max_length=1, default='U',
                              choices=[(key,value) for key, value in STATUSES.items()])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='+')
    total_price = models.PositiveBigIntegerField(default=0)
    code = models.CharField(max_length=10, default=None, null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order { self.id}'
    
    def get_total_cost(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def status_name(self):
        return self.__class__.STATUSES[self.status]

class OrderItem(models.Model):
    class Meta:
        verbose_name, verbose_name_plural = "Order Item", "Order Items"
        



    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='order_items')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.id)
    
    def get_cost(self):
        return self.price * self.quantity
    
