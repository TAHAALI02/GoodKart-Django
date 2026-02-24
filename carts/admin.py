from django.contrib import admin
from .models import *

# Register your models here.
class CartsAdmin(admin.ModelAdmin):
    list_display = ['cart_id','date_added']
    # search_fields = ['product_name']
admin.site.register(cart,CartsAdmin)

class cartitemadmin(admin.ModelAdmin):
    list_display = ['product','cart','quantity','is_active']

admin.site.register(cart_item,cartitemadmin)