from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin
from .forms import CustomerCreationForm, CustomerChangeForm
from .models import Customer


Customer = get_user_model()

class CustomerAdmin(UserAdmin):
    model = Customer
    add_form = CustomerCreationForm
    form = CustomerChangeForm
    list_display = ['phone','email', 'username', 'is_staff']
    # fieldsets = UserAdmin.fieldsets + ((None, {"fields": [],}),)
    # add_fieldsets = UserAdmin.add_fieldsets + ((None,{"fields": ()}),)

admin.site.register(Customer, CustomerAdmin)
