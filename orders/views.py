from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db import transaction
from cart.models import CartItem
from cart.views import _get_cart
from users.models import Address
from .models import Order, OrderItem

@login_required
def create_order(request):
    cart = _get_cart(request)
    cart_items = CartItem.objects.filter(cart=cart)

    if not cart_items.exists():
        return redirect('cart:cart_detail')

    if request.method == 'POST':
        selected = request.POST.get('address')

        if selected == 'new':
            fields = ['postal_code', 'prefecture', 'city', 'street', 'building']
            data = {field: request.POST.get(field) for field in fields}

            if not all(data.values()):
                return render(request, 'orders/order_confirm.html', {
                    'cart_items': cart_items,
                    'total_price': sum(item.product.price * item.quantity for item in cart_items),
                    'addresses': request.user.addresses.all(),
                    'address_error': 'すべての住所項目を入力してください。'
                })

            used_address = Address.objects.create(user=request.user, **data) if 'save_address' in request.POST else Address(**data)
            if not used_address.pk:
                used_address.save()
        else:
            used_address = Address.objects.get(id=selected, user=request.user)

        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=sum(item.product.price * item.quantity for item in cart_items),
                address=used_address
            )

            OrderItem.objects.bulk_create([
                OrderItem(order=order, product=item.product, quantity=item.quantity, price=item.product.price)
                for item in cart_items
            ])

            cart_items.delete()

        return render(request, 'orders/order_complete.html', {'order': order})

    total_price = sum(item.product.price * item.quantity for item in cart_items)
    addresses = request.user.addresses.all()
    return render(request, 'orders/order_confirm.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'addresses': addresses
    })
