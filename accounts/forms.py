from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import Customer, Address
from django.contrib.auth import get_user_model



Customer = get_user_model()

class CustomerCreationForm(forms.ModelForm):
    password = forms.CharField(label='password',widget=forms.PasswordInput)
    password2 = forms.CharField(label='repeat password', widget=forms.PasswordInput)


    class Meta(UserCreationForm):
        model = Customer
        fields = ['username', 'email', 'phone', 'gender']
    
    def clead_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Password does not match.')
        return cd['password2']



class CustomerChangeForm(UserChangeForm):

    class Meta(UserChangeForm):
        model = Customer
        fields = UserChangeForm.Meta.fields
        

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ['customer', 'create_timestamp', 'modify_timestamp']

