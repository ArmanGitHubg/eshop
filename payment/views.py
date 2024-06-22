from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
import stripe
from django.conf import settings
from orders.models import Order
from decimal import Decimal


# Create your views here.


stripe.api_key = settings.STRIPE_SECRET_KEY
stripe.api_version = settings.STRIPE_API_VERSION



def payment_process(request):
    order_id = request.session.get('order_id', None)
    order = get_object_or_404(Order, id=order_id)
    
    if request.method == 'POST':
        success_url = request.build_absolute_uri(reverse('payment:completed'))
        cancel_url = request.build_absolute_uri(reverse('payment:canceled'))
        # stripe checkout session data
        session_data = {
            'mode': 'payment',
            'client_reference_id': order.id,
            'success_url': success_url,
            'cancel_url': cancel_url,
            'line_items': [], 
            

        }
        # add order items to the stripe checkout sesion
        for item in order.items.all():
            session_data['line_items'].append({
                'price_data': {
                    'unit_amount': int(item.price * Decimal('100')),
                    'currency': 'aed',
                    'product_data':{
                        'name': item.product.title,
                    },
                },
                'quantity': item.quantity,
            })
        # create stripe checkout session
        session = stripe.checkout.Session.create(**session_data)
        # redirect to stripe payment form
        return redirect(session.url, code=303)
    else:
        return render(request, 'payment/process.html', locals())

def payment_success(request):
    return render(request, 'payment/completed.html')


def payment_cancel(request):
    return render(request, 'payment/canceled.html')

