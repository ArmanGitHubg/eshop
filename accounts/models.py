from typing import Any
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import EmailValidator
from django.utils import timezone
# Create your models here.


class Customer(AbstractUser):

    
    class Meta:
        verbose_name, verbose_name_plural = ('Customer'), ('Customers')

    
    # active_customers = CustomerManager()
    # USERNAME_FIELD = "phone"
    # USERNAME_FIELD = 'phone'
    # REQUIRED_FIELDS = ['']

    GENDERS = {
        'M': ("male"),
        'F': ("Female"),

    }
    email = models.EmailField("email address", max_length=254, null=False, blank=False,
                               unique=True, validators=[EmailValidator])
    phone = models.CharField(max_length=15, help_text='0501234567', blank=False, null=False, unique=True)
    gender = models.CharField(max_length=1, blank=False, null=False, default='M',
                              choices=[(key, value) for key, value in GENDERS.items()])
    deleted = models.BooleanField(default=False, db_index=True)
    create_timestamp = models.DateTimeField( auto_now_add=True)
    modify_timestamp = models.DateTimeField(auto_now=True)
    delete_timestamp = models.DateTimeField(default=None, null=True,blank=True)

    
    # objects = models.Manager()

    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.phone = self.USERNAME_FIELD


    # def delete(self): # Logical delete
    #     """
    #     override the delete method to logical delete. save the record without show
    #     """
    #     self.deleted =True
    #     self.delete_timestamp = timezone.now()
    #     self.save()
    def __str__(self):
        return self.username


class Address(models.Model):
    class Meta:
        verbose_name, verbose_name_plural = ("Address"), ("Address")

    TYPES = {
        'H': ("Home"),
        'O': ("Office"),
    }

    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, related_name="addresses")
    country = models.CharField(max_length=25, default="UAE")
    state = models.CharField(max_length=15)
    city = models.CharField(max_length=15)
    address = models.TextField()
    type = models.CharField(max_length=1, 
                            choices=[(key, value) for key, value in TYPES.items()])
    create_timestamp = models.DateTimeField(default=timezone.now)
    modify_timestamp = models.DateTimeField(default=timezone.now)

    
    def __str__(self):
        return f"{self.address}-{self.state}-{self.city},{self.country}"
    
    @property
    def billing_type(self):
        return self.__class__.TYPES[self.type]
