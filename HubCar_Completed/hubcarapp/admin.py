from django.contrib import admin

# Register your models here.
from hubcarapp.models import Garage, Customer, Driver, Item, Order, OrderDetails

admin.site.register(Garage)
admin.site.register(Customer)
admin.site.register(Driver)
admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderDetails)
