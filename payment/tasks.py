from celery import shared_task
from io import BytesIO
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.conf import settings
import weasyprint
from orders.models import Order



@shared_task
def payment_completed(order_id):
    """
        task to send an e-mail notification when an order
        is successfully paid.
    """

    order = Order.objects.get(id=order_id)

    # create invoice e-mail
    subject = f'Ecom - Invoice no. {order.id}'
    message = 'Please, find the attached the invoice for your recent purchase.'
    email = EmailMessage(subject,
                         message,
                         'admin@ecom.com',
                         [order.customer.email])
    
    # generate pdf
    html = render_to_string('orders/order/pdf.html',{'order':order})
    out = BytesIO()
    stylesheets = [weasyprint.CSS(settings.STATIC_ROOT / 'css/pdf.css')]
    weasyprint.HTML(string=html).write_pdf(out, stylesheets=stylesheets)

    # attach pdf file

    email.attach(f'order_{order.id}.pdf',
                  out.getvalue(),
                  'application/pdf')
    
    # send e-mail
    email.send()

