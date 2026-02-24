from django.shortcuts import render
from store.models import product

def home(request):
    products = product.objects.all().filter(is_available=True)
    products_count = products.count()
    context = {
        'products': products,
        'products_count': products_count
    }
    return render(request,'home.html',context)