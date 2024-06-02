from django.shortcuts import render, redirect, HttpResponse
from cart.cart import Cart
from accounts.models import Customer, Address
from django.shortcuts import get_object_or_404
from .forms import OrderCreateForm, OrderItemCreateForm
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .models import Order, OrderItem

# Create your views here.

class OrderCreateView(CreateView):
    model = Order


    def get(self, request, *args, **kwargs):
        cart = Cart(request)
        
        customer = get_object_or_404(Customer, id = request.user.id)
        address = customer.addresses.first()
        total_price= cart.get_total_price()
        # order = Order.objects.create(customer=customer,
        #                              address = address,
        #                              total_price=total_price)
        form = OrderCreateForm(initial={
            'customer': customer,
            'address': address,
            'total_price': total_price,
        })
        return render(request, "order/order_create.html",
                       context={'cart':cart,
                                'form': form,
                                'customer': customer,
                                'address': address,
                                })

    def post(self, request, *args, **kwargs):
        cart = Cart(request)
        
        customer = get_object_or_404(Customer, id=request.user.id)
        address = customer.addresses.first()
        if not address:
            return redirect('profile_add')
        # address = get_object_or_404(Address, customer=customer)
        total_price = cart.get_total_price()

        # order = Order.objects.create(customer=customer,
        #                              address=address,
        #                              total_price=total_price)
        
        form = OrderCreateForm(request.POST)
        
        if form.is_valid():

            
            order = form.save()
            for item in cart:
                OrderItem.objects.create(
                    order=order,
                    product = item['product'],
                    price= item['price'],
                    quantity = item['quantity'],
                )
            
            # for item in cart:
            #     OrderItem.objects.create(
            #         order = order,
            #         product = item['product'],
            #         price = item['price'],
            #         qantity = item['quantity']
            #     )
        else:
            return HttpResponse('<h1>the form is incorrect<h1>') 
        cart.clear()
        return render(request, 'order/order_created.html',
                      context={'order':order,
                               })



class OrderCreatedView(TemplateView):
    template_name = "order/order_created.html"
    



# from django.shortcuts import render
# from .models import OrderItem
# from .forms import OrderCreateForm
# from cart.cart import Cart
# def order_create(request):
#     cart = Cart(request)
#     if request.method == 'POST':
#         form = OrderCreateForm(request.POST)
#         if form.is_valid():
#             order = form.save()
#             for item in cart:
#                 OrderItem.objects.create(order=order,
#                             product=item['product'],
#                             price=item['price'],
#                             quantity=item['quantity'])
#         # clear the cart
#             cart.clear()

#         return render(request,
#                 'orders/order/created.html',
#                         {'order': order})
#     else:
#         form = OrderCreateForm()
#     return render(request,
#                 'orders/order/create.html',
#                 {'cart': cart, 'form': form})