from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Product
from django.contrib.auth.models import User
from cart.models import Cart, CartItem
from users.models import Credit


def index(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            login(request, User.objects.get(username=username))
        else:
            user = User.objects.create_user(username=username, password=password)
            Credit.objects.create(user=user)
            login(request, user)
        for cart in Cart.objects.all():
            cart.delete_cart_items()
            cart.delete()
        Cart.objects.create(user=request.user)
    return render(request, 'base/home.html')


@login_required
def snacks(request):
    process_cart_add(request)
    context = {
        'products': Product.objects.filter(snack=True)
    }
    return render(request, 'base/product_list.html', context)


@login_required
def drinks(request):
    process_cart_add(request)
    context = {
        'products': Product.objects.filter(drink=True)
    }
    return render(request, 'base/product_list.html', context)


@login_required
def special(request):
    process_cart_add(request)
    context = {
        'products': Product.objects.filter(special=True)
    }
    return render(request, 'base/product_list.html', context)


def process_cart_add(request):
    if request.method == "POST":
        product = Product.objects.get(id=request.POST['product_id'])
        quantity = int(request.POST['quantity'])
        cart = Cart.objects.get(user=request.user)
        if CartItem.objects.filter(item=product).exists():
            cart_item = CartItem.objects.get(item=product)
            cart_item.quantity += quantity
            cart_item.save()
        else:
            cart_item = CartItem.objects.create(item=product, quantity=quantity)
        cart.items.add(cart_item)
