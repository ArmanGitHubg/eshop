from django.shortcuts import render, redirect, HttpResponse
from django.urls import reverse
from cart.cart import Cart
from accounts.models import Customer, Address
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .forms import OrderCreateForm, OrderItemCreateForm
from django.views.generic.edit import CreateView
from django.views.generic import TemplateView
from .models import Order, OrderItem
from django.template.loader import render_to_string

from .tasks import order_created
import weasyprint
from django.conf import settings

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
            if cart.coupon:
                order.coupon = cart.coupon
                order.discount = cart.coupon.discount
            order.save()
            
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
        
            cart.clear()

            # launch asynchronous task
            order_created.delay(order.id)
            request.session['order_id'] = order.id

        # return render(request, 'order/order_created.html',
        #               context={'order':order,
        #                        })
            return redirect(reverse('payment:process'))


class OrderCreatedView(TemplateView):
    template_name = "order/order_created.html"
    

@staff_member_required
def admin_order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    return render(request, 'admin/orders/order/detail.html',{'order':order})

@staff_member_required
def admin_order_pdf(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    html = render_to_string('orders/order/pdf.html', {'order':order})
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposititon'] = f'filename=order_{order.id}.pdf'
    weasyprint.HTML(string=html).write_pdf(response, stylesheets=[weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')])
    return response

