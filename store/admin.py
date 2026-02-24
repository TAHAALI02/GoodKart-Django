from django.contrib import admin
from .models import *


# Register your models here.
class productAdmin(admin.ModelAdmin):
    list_display = ('product_name','description','price','stock','is_available','created_at','modified_at')
    prepopulated_fields = {'slug':('product_name',)}
admin.site.register(product,productAdmin)