import datetime
import time

from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Cart
from django.contrib.auth.models import User


def write_log(user: User, cart: Cart):
    filename = "logs/" + user.username + str(time.time()) + '.txt'
    with open(filename, 'w') as f:
        f.write(f'User: {user.username}\n')
        f.write(f'Date: {datetime.datetime.now()}\n')
        f.write(f'Starting Credit: ${user.credit.credit}\n')
        f.write(f'Ending Credit: ${user.credit.credit - cart.get_total_cart_price()}\n')
        f.write(f'Items:\n')
        f.write('\n')
        for item in cart.items.all():
            f.write(f'    {item.item.name} - {item.quantity}    ${item.get_total_price()}\n')
        f.write('\n')
        f.write(f'Total: ${cart.get_total_cart_price()}\n')


@login_required
def index(request):
    if request.method == 'POST':
        if request.POST['checkout'] == "True":
            if request.POST.get('cash', True) == "True":
                write_log(request.user, Cart.objects.get(user=request.user))
                print("skipped")
            else:
                write_log(request.user, Cart.objects.get(user=request.user))
                print(request.user.credit.credit)
                request.user.credit.credit -= Cart.objects.get(user=request.user).get_total_cart_price()
                print(request.user.credit.credit)
                request.user.credit.save()
            # handle checkout and logout the user
            Cart.objects.get(user=request.user).delete_cart_items()
            Cart.objects.get(user=request.user).delete()
            logout(request)
            return redirect('home')
    context = {
        'items': Cart.objects.get(user=request.user).items.all(),
        'cart': Cart.objects.get(user=request.user),
        'user': request.user,
    }
    return render(request, 'cart/cart.html', context)
