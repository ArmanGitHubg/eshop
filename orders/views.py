from django.shortcuts import render, redirect
from cart.cart import Cart
from .forms import OrderForm, OrderItemForm
from django.views.generic import View

# Create your views here.

class OrderCreateView(View):

    def get(self, request, *args, **kwargs):
        