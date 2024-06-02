from typing import Any
from django.db.models.query import QuerySet
from django.shortcuts import render, redirect
from .models import Category, Brand, Discount, Product
from django.views.generic import ListView, DetailView, View
from django.shortcuts import get_object_or_404, get_list_or_404
from cart.forms import CartAddProductForm
from cart.cart import Cart
# Create your views here.

class ProductListView(ListView):
    
    # def get(self, request, *args, **kwargs):
    #     products = Product.objects.all()
    #     products.order_by('-id')
    #     return render(request,'products/product_list.html',
    #                   {'products': products})

    context_object_name = "products"
    paginate_by = 12

    def get_queryset(self):
        result = Product.objects.all()
        kwargs = self.request.GET
        if "category" in kwargs:
            result = result.filter(category__slug=kwargs["category"])
        if "brand" in kwargs:
            result = result.filter(brand__slug=kwargs["brand"])
        return result
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        return context


    
class ProductDetailView(DetailView):


  
    model = Product
    # context_object_name = "product"
    template_name = 'products/product_detail.html'
    
    def get(self, request, slug, *args, **kwargs):
        form = CartAddProductForm()
        product = get_object_or_404(Product,slug=slug)

        return render(request, 'products/product_detail.html',
                        {'product':product,
                         'form':form})

    
    def post(self, request, slug, *args, **kwargs):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddProductForm(request.POST)
        cart = Cart(request)

        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product, quantity=cd['quantity'])

            return redirect('cart:cart_detail')



class CategoryListView(ListView):
    
    # to override the default context 'object_list'
    context_object_name = 'parents'
    template_name = 'products/category_list.html'
    # to define the or retrive the custom queried data as context('parents')
    def get_queryset(self):
        parents =  Category.objects.filter(root=None)
        return parents

    # for additional context data to supply as context data
    def get_context_data(self, **kwargs: Any): 
        context = super().get_context_data(**kwargs)
        return context 