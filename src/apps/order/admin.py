from django.contrib import admin
from .models import Order, Address, OrderProduct
# Register your models here.
admin.site.register(Order)
admin.site.register(Address)    
admin.site.register(OrderProduct)