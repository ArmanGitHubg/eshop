from django.urls import path

from . import views

app_name = 'product'

urlpatterns = [
    path('', views.ProductListView.as_view(), name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    # path('<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('<str:slug>/',views.ProductDetailView.as_view(), name='product_detail'),
    path('categories/', views.CategoryListView.as_view(), name='category_list'),
]