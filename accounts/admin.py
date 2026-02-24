from django.contrib import admin
from .models import *
from django.contrib.auth.admin import UserAdmin

# class AccountAdmin(admin.ModelAdmin):
#     list_display = ['first_name','last_name','email','phone_number','is_active','is_staff','is_admin','is_superuser']

# this is same as AccountAdmin but in this we can't change password form admin panel
class MyAccountManager(UserAdmin):
    list_display = ['first_name','last_name','email','phone_number','date_joined','last_login','is_active','is_staff','is_admin','is_superuser']

    list_display_links = ['email','first_name','last_name']
    readonly_fields = ['date_joined','last_login']
    ordering = ('-date_joined',)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


# Register your models here.
admin.site.register(Account,MyAccountManager)