from django.contrib import admin
from .models import Category, Brand, Discount, Product

# Register your models here.
class BasicTabularInline(admin.TabularInline):
    fields = [('name', 'slug')]
    prepopulated_fields = {'slug':('name',)}
    extra = 1

class BasicStackedInline(admin.StackedInline):
    fields =[('title', 'slug')]
    prepopulated_fields = {'slug': ('title',)}
    extra = 1

class CategoryInline(BasicTabularInline):
    model = Category

class ProductInline(BasicStackedInline):
    model = Product
    fields = BasicTabularInline.fields + [
        'category', 'price', 'discount'
    ]





@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price', 'final_price', 'discount', 'category', 'brand', 'status', ]
    list_filter = ['status', 'title', 'price', 'discount', 'category', 'brand']
    search_fields = ['title', 'category', 'brand']
    prepopulated_fields = {'slug': ['title']}
    list_editable = ['price', 'discount']




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    list_filter = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug': ['name']}
    ordering = ['id']
    inlines = [CategoryInline]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug','logo']
    list_filter = ['name']
    search_fields = ['name']
    prepopulated_fields = {'slug':['name']}
    ordering = ['id']
    inlines = [ProductInline]


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ['amount', 'start_date', 'end_date']
    list_filter = ['start_date', 'end_date']
