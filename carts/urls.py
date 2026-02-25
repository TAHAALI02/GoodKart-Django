from django.urls import path
from . import views as v



urlpatterns = [
    path('', v.cart, name='cart'),
    path('add_cart/<int:product_id>/', v.add_cart, name='add_cart'),
    path('remove_cart/<int:product_id>/', v.remove_cart, name='remove_cart'),
    path('remove_cart_item/<int:product_id>/', v.remove_cart_item, name='remove_cart_item'),

]