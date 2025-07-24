from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from cart.models import CartItem
from .models import Order, OrderItem
from django.db import transaction

@login_required
def create_order(request):
    cart = request.user.carts.first()
    if not cart:
        return redirect('cart:cart_detail')

    cart_items = CartItem.objects.filter(cart=cart)
    if not cart_items.exists():
        return redirect('cart:cart_detail')
    
    if request.method == 'POST':
        selected = request.POST.get('selected_address')

        # 新しい住所を入力した場合
        if selected == 'new':
            postal_code = request.POST.get('postal_code')
            prefecture = request.POST.get('prefecture')
            city = request.POST.get('city')
            detail = request.POST.get('detail')

            if not all([postal_code,prefecture, city, detail]):
                return render(request, 'orders/order_confirm.html', {
                    'cart_items': cart_items,
                    'total_price': sum(item.product.price * item.quantity for item in cart_items),
                    'address_error': 'すべての住所項目を入力してください。',
                    'addresses': request.user.address_set.all()
                })
            
            # チェックボックスがオンなら保存
            if request.POST.get('save_address'):
                new_address = Address.objects.create(
                    user=request.user,
                    postal_code=postal_code,
                    prefecture=prefecture,
                    city=city,
                    detail=detail
                )
            else:
                new_address = Address(
                    postal_code=postal_code,
                    prefecture=prefecture,
                    city=city,
                    detail=detail
                )

            used_address = new_address

        else:
            used_address = Address.objects.get(id=selected, user=request.user)


        with transaction.atomic():
            order = Order.objects.create(
                user=request.user,
                total_price=sum(item.product.price * item.quantity for item in cart_items),
                address=used_address
            )

            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart_items.delete() # カートを空にする

        return render(request, 'orders/order_complete.html', {'order': order})
    
    else:
        # GETなら確認ページを表示
        total_price = sum(item.product.price * item.quantity for item in cart_items)
        address = request.user.profile.address
        return render(request, 'orders/order_confirm.html', {
            'cart_items': cart_items,
            'total_price': total_price,
            'address': address
        })