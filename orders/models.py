from django.db import models
from accounts.models import Customer, Address
from products.models import Product
from django.conf import settings
from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from coupons.models import Coupon

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
    stripe_id = models.CharField(max_length=250, blank=True)

    status = models.CharField(max_length=1, default='U',
                              choices=[(key,value) for key, value in STATUSES.items()])
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name='orders')
    # address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='adresses')
    address = models.CharField()
    total_price = models.PositiveBigIntegerField(default=0)
    code = models.CharField(max_length=10, default=None, null=True, blank=True)
    coupon = models.ForeignKey(Coupon, related_name='orders', null=True, blank=True, on_delete=models.SET_NULL)
    discount = models.IntegerField(default=0, validators=[MinValueValidator(0),
                                   MaxValueValidator(100)])
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Order { self.id}'
    
    def get_total_cost(self):
        total_cost = self.get_total_cost_before_discount()
        return total_cost - self.get_discount()
    
    def status_name(self):
        return self.__class__.STATUSES[self.status]
    
    def get_stripe_url(self):
        if not self.stripe_id:
            # no payment associated
            return
        if '_test_' in settings.STRIPE_SECRET_KEY:
            # stripe path for payment
            path = '/test/'
        else:
            # stripe path for real payments
            path = '/'
        return f'https://dashboard.stripe.com{path}payments/{self.stripe_id}'
    
    def get_total_cost_before_discount(self):
        return sum(item.get_cost() for item in self.items.all())
    
    def get_discount(self):
        total_cost = self.get_total_cost_before_discount()
        if self.discount:
            return total_cost * (self.discount/Decimal(100))
        return Decimal(0)


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
    
