from django import forms
from .models import Order, OrderItem



class OrderItemCreateForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['order', 'product', 'price', 'quantity']
        widgets = {
            # 'order': forms.HiddenInput(),
            # 'product': forms.HiddenInput(),
            # 'price': forms.HiddenInput(),
            # 'quantity': forms.HiddenInput(),
        }


class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['status','customer', 'total_price', 'address', 'code']
        widgets = {
            'status': forms.HiddenInput(),
            'customer': forms.HiddenInput(),
            'total_price': forms.HiddenInput(),
            'discount': forms.HiddenInput(),
            'address': forms.HiddenInput(),
            'code': forms.HiddenInput(),
        }