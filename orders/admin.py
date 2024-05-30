from django.contrib import admin
from .models import Order, OrderItem
# Register your models here.

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    # fields  = ['product', 'price','quantity' ]
    raw_id_fields = ['product']
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    model = Order
    list_display = ['id', 'status', 'customer', 'address', 'total_price', 'created_at', 'updated_at']
    list_filter = ['status', 'created_at', 'updated_at']
    inlines = [OrderItemInline]

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    model = OrderItem
    list_display = ['__str__', 'order', 'product', 'price', 'quantity']
    ordering = ('-id',)
    search_fields = ('order', 'product')


