from django.contrib import admin
from django.urls import path
from . import views as v



urlpatterns = [
    # path('/', v.home, name='home'),
    path('', v.store, name='store'),
    path('category/<slug:category_slug>/', v.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', v.product_details, name='product_details'),
    path('search/', v.search, name='search'),
]