from django.shortcuts import render,redirect,HttpResponse,get_object_or_404
from store.models import product as Product
from store.models import variation
from .models import cart as Cart,cart_item as CartItem
from django.core.exceptions import ObjectDoesNotExist
# Create your views here.


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def add_cart(request,product_id):
    product = Product.objects.get(id=product_id) # get product
    product_variation = []
    if request.method == 'POST':
        for item in request.POST:
            key = item
            value = request.POST[key]
            # print(key,value)
            try:
                variations = variation.objects.get(product=product,variation_name__iexact=key,variation_value__iexact=value)
                product_variation.append(variations)
            except:
                print('error')


    try:
        cart=Cart.objects.get(cart_id=_cart_id(request)) # get the cart using the cart_id present in session
    except Cart.DoesNotExist:
        cart = Cart.objects.create(
            cart_id=_cart_id(request),
        )
        cart.save()

    try:
        cart_item = CartItem.objects.get(product=product,cart=cart)
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
        cart_item.quantity += 1
        cart_item.save()
    except CartItem.DoesNotExist:

        cart_item = CartItem.objects.create(
            product=product,
            cart=cart,
            quantity=1
        )
        if len(product_variation) > 0:
            cart_item.variation.clear()
            for item in product_variation:
                cart_item.variation.add(item)
        cart_item.save()

    return redirect('cart')


def remove_cart(request, product_id):
    try:
        carts = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(product=product, cart=carts)

        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()

    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        pass

    return redirect('cart')

def remove_cart_item(request, product_id):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        product = get_object_or_404(Product, id=product_id)
        cart_item = CartItem.objects.get(cart=cart,product=product)
        cart_item.delete()
    except (Cart.DoesNotExist, CartItem.DoesNotExist):
        pass
    return redirect('cart')

def cart(request,total=0,quantity=0,cart_item=None):
    cart_items = []
    tax = 0
    grand_total = 0
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart,is_active=True)
        for item in cart_items:
            total += (item.product.price * item.quantity)
            quantity += item.quantity
        tax = (total*5)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass
    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'grand_total': grand_total,
        'tax': tax
    }
    return render(request,'store/cart.html',context)