from django.shortcuts import render
from .forms import CartAddProductForm
from .cart import Cart
from products.models import Product
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import DetailView, View
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
        cart = Cart(request)
        for item in cart:
            item['update_quantity_form']= CartAddProductForm(initial={
                'quantity': item['quantity'],
                'override': True,
            })
        return render(request, self.template_name, context={'cart':cart})
    
    

    # def get_queryset(self, request):
    #     cart = Cart(request)
    #     return cart
        
            

