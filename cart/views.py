from django.shortcuts import render
from django.urls import reverse
from .forms import CartAddProductForm
from .cart import Cart
from products.models import Product
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View

from coupons.forms import CouponApplyForm
from products.recommender import Recommender

# Create your views here.


class CartAddView(View):
    
    
    def post(self, request, product_id, *args, **kwargs):

        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        form = CartAddProductForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            cart.add(product=product,
                     quantity=cd['quantity'],
                     override=cd['override'])
        return redirect('cart:cart_detail')
    
class CartRemoveView(View):
    def post(self, request, product_id, *args, **kwargs):
        cart = Cart(request)
        product = get_object_or_404(Product, id=product_id)
        # form = CartAddProductForm(request.POST)
        # if form.is_valid():
        #     cd = form.cleaned_data
            
        cart.remove(product)
        return redirect('cart:cart_detail')
    
class CartDetailView(View):
    
    context_object_name = 'cart'
    template_name = 'cart/cart_detail.html'
    def get(self, request, *args, **kwargs):
        coupon_apply_form = CouponApplyForm()
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form']= CartAddProductForm(initial={
                'quantity': item['quantity'],
                'override': True,
            })
        r = Recommender()
        cart_products = [item['product'] for item in cart]
        if (cart_products):
            recommended_products = r.suggest_products_for(cart_products, max_results=4)
        else:
            recommended_products = []


        return render(request, self.template_name, context={'cart':cart,
                                                            'coupon_apply_form': coupon_apply_form,
                                                            'recommended_products':recommended_products})
    
    

    # def get_queryset(self, request):
    #     cart = Cart(request)
    #     return cart
        
            

