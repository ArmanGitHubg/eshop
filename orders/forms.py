from django import forms
from .models import Order, OrderItem



class OrderItemForm(forms.ModelForm):
    pass


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        widgets = {
            'status': forms.HiddenInput(),
            'customer': forms.HiddenInput(),
            'total_price': forms.HiddenInput(),
            'discount': forms.HiddenInput(),
        }