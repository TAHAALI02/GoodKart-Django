from django.contrib import admin

from .models import *

# Register your models here.
class admincategroy(admin.ModelAdmin):
    prepopulated_fields = {'slug':('category_name',)}
    list_display = ['category_name','slug','description','cat_image']
admin.site.register(category,admincategroy)