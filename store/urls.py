from django.contrib import admin
from django.urls import path
from . import views as v



urlpatterns = [
    # path('/', v.home, name='home'),
    path('', v.store, name='store'),
    path('<slug:category_slug>/', v.store, name='products_by_category'),
    path('<slug:category_slug>/<slug:product_slug>/', v.product_details, name='product_details'),
]