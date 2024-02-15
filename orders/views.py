
from .tasks import order_created
from django.urls import reverse

from django.shortcuts import render, redirect
from .models import OrderItem
from .forms import OrderCreationForm
from cart.cart import Cart

# Create your views here.

def order_create(request):
    cart = Cart(request)
    if request.method == 'POST':
        form = OrderCreationForm(request.POST)
        if form.is_valid():
            order = form.save()
            for item in cart:
                OrderItem.objects.create(order=order,
                                        product=item['product'],
                                        price=item['price'],
                                        quantity=item['quantity'])
            # clear the cart
            cart.clear()
            order_created.delay(order.id)

            # set order of
            request.session['order_id'] = order.id
            return  redirect(reverse('payment:process'))
            # return render(request,
            #               'orders/order/created.html',
            #               {'order': order})
    else:
        form = OrderCreationForm()
    return render(request,
                  'orders/order/create.html',
                  {'cart': cart, 'form': form})
                  