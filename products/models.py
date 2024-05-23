from django.db import models
from django.utils import timezone

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    root = models.ForeignKey('self', default=None, null=True,
                              blank=True, on_delete=models.SET_NULL, related_name='subcategories')
    
    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['name']),
            ]
        verbose_name, verbose_name_plural = 'category', 'categories'

    def __str__(self) -> str:
        return self.name
    
class Brand(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    logo = models.FileField(upload_to='product/brands/', default='unknown.jpg', blank=True)
    website = models.CharField(max_length=200, default=None, null=True,blank=True )

    class Meta:
        verbose_name, verbose_name_plural = 'brand', 'brands'
        ordering = ['name']
        indexes =[
            models.Index(fields=['name']),

        ]
    def __str__(self) -> str:
        return self.name
    
class Discount(models.Model):
    class Meta:
        verbose_name, verbose_name_plural = 'discount', 'discounts'

    amount = models.PositiveBigIntegerField(default=0, null=True, blank=True)
    start_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    end_date = models.DateTimeField(default=None, null=True, blank=True)

    def calculate_price(self, price: int) -> int:
        decrease, present = 0, timezone.now()
        if self.start_date <= present :
            if self.end_date is None or present <= self.end_date:
                percentage = self.amount / 100
                decrease_amount = price * percentage
                decrease = price - decrease_amount
        return max(decrease, 0)
    
    def __str__(self) -> str:
        return f"{self.amount}%"
    

class Product(models.Model):
    class Meta:
        verbose_name, verbose_name_plural = 'product', 'products'

    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    image = models.FileField(upload_to='product/products', default='unknown.jpg', blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name='products')
    price = models.PositiveBigIntegerField()
    description = models.TextField()
    status = models.BooleanField(default=True)
    discount = models.ForeignKey(Discount, on_delete=models.CASCADE, related_name='products', default=None, null=True, blank=True)
    create_timestamp = models.DateField(auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)
    
    @property
    def final_price(self) -> int:
        result = self.price
        if self.discount is not None:
            result = self.discount.calculate_price(result)
            
        return result

    def __str__(self) -> str:
        return f"{self.title}-$({self.price})- ({self.discount}%)"
    