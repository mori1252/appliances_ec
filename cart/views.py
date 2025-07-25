from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from products.models import Product
from .models import Cart, CartItem

def _get_cart(request):
    print("=== _get_cart called ===")
    
    if request.user.is_authenticated:
        print(f"ログインユーザー: {request.user}")
        cart, created = Cart.objects.get_or_create(user=request.user)
        print(f"カート取得: {cart}（新規作成: {created}）")
    else:
        session_key = request.session.session_key
        print(f"初期セッションキー: {session_key}")

        if not session_key:
            request.session.create()
            session_key = request.session.session_key
            print(f"新規セッションキー作成: {session_key}")

        # セッション保存（念のため）
        request.session.modified = True
        request.session.save()

        if session_key:
            cart, created = Cart.objects.get_or_create(session_key=session_key)
            print(f"ゲスト用カート取得: {cart}（新規作成: {created}）")
        else:
            print("セッションキーが取得できませんでした")
            cart = None

    return cart



def cart_detail(request):
    cart = _get_cart(request)
    items = cart.items.select_related('product') if cart else []
    total = sum(item.get_total_price() for item in items)
    return render(request, 'cart/cart_detail.html', {
        'cart': cart,
        'items': items,
        'total': total,
    })

def add_to_cart(request, product_id):
    cart = _get_cart(request)
    product = get_object_or_404(Product, id=product_id)

    #すでにカートに入っている場合は数量を増やす
    cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart:cart_detail')

def remove_from_cart(request, item_id):
    item = get_object_or_404(CartItem, id=item_id)
    item.delete()
    return redirect('cart:cart_detail')

def update_cart_item_quantity(request, item_id):
    # POSTで数量を更新（例：フォーム送信）
    item = get_object_or_404(CartItem, id=item_id)
    if request.method == 'POST':
        try:
            new_quantity = int(request.POST.get('quantity', 1))
            if new_quantity > 0:
                item.quantity = new_quantity
                item.save()
            else:
                item.delete() # 数量0は削除扱い
        except ValueError:
            pass # 不正な数値が送られた場合は何もしない
    return redirect('cart:cart_detail')

