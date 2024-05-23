from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import TemplateView
from django.views.generic import DetailView
from .forms import CustomerCreationForm, AddressForm
from django.views.generic import View
from django.contrib.auth import get_user_model
from .models import Customer, Address

# Create your views here.
class HomePageView(TemplateView):
    template_name = 'home.html'
    context = {'section': 'home'}
    
class CustomerRegistrationView(View):
    template_name = 'registration/user_registration.html'
    user_form = CustomerCreationForm
    context = {'user_form': user_form}

    def get(self,request):
        user_form = self.user_form
        return render(request, self.template_name, self.context)
    
    def post(self,request):
        user_form = self.user_form(request.POST)
        
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            
            return render(request, 'registration/registration_done.html')
        else:

            return render(request,self.template_name, self.context)

class ProfileView(View):
    # address = Address
    # template_name = 'account/profile.html'
    # context = {'address': address}
    def get(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist:
            return redirect(reverse('logout'))
        try: 
            address = customer.addresses.all()
        except Address.DoesNotExist:
            address = None
        
        
        return render(request, 'account/profile.html',
                      {'customer': customer,
                       'address':address})

class ProfileCreateView(View):
    def get(self, request, *args, **kwargs):
        form = AddressForm()
        return render(request, 'account/profile_edit.html',
                      {'form': form, })
    
    def post(self, request, *args, **kwargs):
        form = AddressForm(data=request.POST)
        if form.is_valid():
            new_address = form.save(commit=False)
            try:
                customer = Customer.objects.get(id=request.user.id)
            except Customer.DoesNotExist:
                return redirect('logout')
            new_address.customer = customer
            new_address.save()
            return redirect(reverse('profile'))
        else:
            return render(request, 'account/profile_edit.html',
                          {'form':form,} )


class ProfileEditView(View):
    

    def get(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist:
            return reverse('logout')
        address = Address.objects.get(customer=customer)
        # address = customer.addresses.all()
        if address.customer == customer:
            form = AddressForm(instance=address)
        
            return render(request, 'account/profile_edit.html',
                          {'form':form,})
        
        return redirect(reverse('profile'))

    def post(self, request, *args, **kwargs):
        try:
            customer = Customer.objects.get(id=request.user.id)
        except Customer.DoesNotExist:
            return redirect('logout')
        address = Address.objects.get(customer=customer)
        if address.customer == customer:

            form = AddressForm(data=request.POST, instance=address)
       
            if form.is_valid():
                form.save()
                return redirect(reverse('profile'))
            else:
                return render(request, 'account/profile_edit.html',
                            {'form': form,})
        else:
            return redirect(reverse('profile'))