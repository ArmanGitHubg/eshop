from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('process/', views.payment_process, name='process'),
    path('success/', views.payment_success, name='completed'),
    path('cancel/', views.payment_cancel, name='canceled'),

]
