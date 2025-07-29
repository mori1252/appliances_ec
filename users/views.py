from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Address
from .forms import UserUpdateForm, PasswordUpdateForm, AddressForm, CustomUserCreationForm, CustomLoginForm
from django.http import JsonResponse
import json


# -------------------
# 共通住所保存関数
# -------------------
def save_address(user, data):
    """POSTデータをもとに住所を保存する"""
    Address.objects.create(
        user=user,
        postal_code=data.get('postal_code', ''),
        prefecture=data.get('prefecture', ''),
        city=data.get('city', ''),
        street=data.get('street', ''),
        building=data.get('building', ''),
    )

# -------------------
# デフォルト住所設定（選んだ住所以外デフォルト解除）
# -------------------
def set_default_address(user, current_address):
    # ユーザーの他の住所をすべて is_default=False に
    Address.objects.filter(user=user).exclude(id=current_address.id).update(is_default=False)
    # この住所をデフォルトに
    current_address.is_default = True
    current_address.save()


# -------------------
# カート統合関数（ログイン前呼び出し）
# -------------------
def merge_cart(request, user, session_key):
    if not session_key:
        print("ログイン前のセッションキーがありません")
        return

    session_carts = Cart.objects.filter(session_key=session_key, user__isnull=True)
    if not session_carts.exists():
        print("セッションカートが見つかりません")
        return

    user_cart, _ = Cart.objects.get_or_create(user=user)

    for session_cart in session_carts:
        for item in session_cart.items.all():
            existing_item = user_cart.items.filter(product=item.product).first()
            if existing_item:
                existing_item.quantity += item.quantity
                existing_item.save()
            else:
                CartItem.objects.create(
                    cart=user_cart,
                    product=item.product,
                    quantity=item.quantity
                )
        session_cart.delete()

# -------------------
# ログインビュー
# -------------------
def user_login(request):
    if request.method == 'POST':
        session_key_before_login = request.session.session_key  # ここでセッションキー保存
        form = CustomLoginForm(request, data=request.POST)
        if form.is_valid():
            login(request, form.get_user())
            merge_cart(request, form.get_user(), session_key_before_login)  # セッションキーを渡す
            messages.success(request, "ログインしました。")
            return redirect('products:list')
        else:
            messages.error(request, "ユーザー名またはパスワードが正しくありません。")
    else:
        form = CustomLoginForm()
    return render(request, 'users/login.html', {'form': form})


# -------------------
# ログアウトビュー
# -------------------
def user_logout(request):
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect('products:list')


# -------------------
# 新規登録ビュー
# -------------------
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        address_form = AddressForm(request.POST)

        if form.is_valid() and address_form.is_valid():
            user = form.save()
            login(request, user)

            address = address_form.save(commit=False)
            address.user = user
            # 初回住所の場合のみデフォルトに設定
            if not Address.objects.filter(user=user).exists():
                address.is_default = True
            else:
                address.is_default = False
            address.save()

            messages.success(request, "ユーザー登録が完了しました。")
            return redirect('products:list')
        else:
            messages.error(request, "入力内容に誤りがあります。")
    else:
        form = CustomUserCreationForm()
        address_form = AddressForm()

    return render(request, 'users/register.html', {
        'form': form,
        'address_form': address_form    
    })

# -------------------
# マイページ（ログインユーザー専用）
# -------------------
@login_required
def user_mypage(request):
    user = request.user
    addresses = Address.objects.filter(user=user)
    # GET時・初期表示用
    default_address = addresses.filter(is_default=True).first()
    # 変更: デフォルトアドレスが設定されていない場合は最初の住所をフォールバック
    if default_address is None:
        default_address = addresses.first()

    # 変更: GETリクエストでの削除処理を追加
    delete_id = request.GET.get('address_id')
    if delete_id and 'delete_address' in request.GET:
        try:
            address_to_delete = Address.objects.get(id=delete_id, user=user)
            address_to_delete.delete()
            messages.success(request, '選択中の住所を削除しました。')
        except Address.DoesNotExist:
            pass
        return redirect('users:mypage')

    if request.method == 'POST':
        selected_id = request.POST.get('address_id')
        try:
            selected_address = Address.objects.get(id=selected_id, user=user)
        except Address.DoesNotExist:
            selected_address = default_address

        # ■ 削除ボタン押下時
        if 'delete_address' in request.POST:
            if selected_address:
                selected_address.delete()
                messages.success(request, '選択中の住所を削除しました。')
            return redirect('users:mypage')

        # フォームを作成
        user_form = UserUpdateForm(request.POST, instance=user, prefix='user')
        address_form = AddressForm(request.POST, instance=selected_address, prefix='address')
        password_form = PasswordUpdateForm(user, prefix='password')
        new_address_form = AddressForm(prefix='newaddress')

        if 'update_all' in request.POST:
            if user_form.is_valid() and address_form.is_valid():
                user_form.save()
                addr = address_form.save(commit=False)
                addr.user = user
                addr.is_default = True
                addr.save()
                if 'address-is_default' in request.POST:
                    set_default_address(user, addr)
                messages.success(request, 'ユーザー情報と住所を更新しました。')
                return redirect('users:mypage')
            else:
                messages.error(request, 'ユーザー情報または住所の更新に失敗しました。')

        elif 'save_password' in request.POST:
            password_form = PasswordUpdateForm(user, request.POST, prefix='password')
            user_form = UserUpdateForm(instance=user, prefix='user')
            address_form = AddressForm(instance=default_address, prefix='address')
            new_address_form = AddressForm(prefix='newaddress')

            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, user)
                messages.success(request, 'パスワードを更新しました。')
                return redirect('users:mypage')
            else:
                messages.error(request, 'パスワードの更新に失敗しました。')

        elif 'save_new_address' in request.POST:
            new_address_form = AddressForm(request.POST, prefix='newaddress')
            user_form = UserUpdateForm(instance=user, prefix='user')
            address_form = AddressForm(instance=default_address, prefix='address')
            password_form = PasswordUpdateForm(user, prefix='password')

            if new_address_form.is_valid():
                new_address = new_address_form.save(commit=False)
                new_address.user = user
                new_address.save()
                if 'newaddress-new_is_default' in request.POST:
                    set_default_address(user, new_address)
                messages.success(request, '新しい住所を追加しました。')
                return redirect('users:mypage')
            else:
                messages.error(request, '新しい住所の追加に失敗しました。')
    else:
        # GET時は default_address を選択
        user_form = UserUpdateForm(instance=user, prefix='user')
        password_form = PasswordUpdateForm(user, prefix='password')
        address_form = AddressForm(instance=default_address, prefix='address')
        new_address_form = AddressForm(prefix='newaddress')
        selected_address = default_address

    addresses_json = json.dumps([{
        'id': addr.id,
        'postal_code': addr.postal_code,
        'prefecture': addr.prefecture,
        'city': addr.city,
        'street': addr.street,
        'building': addr.building,
        'is_default': addr.is_default,
    } for addr in addresses])

    return render(request, 'users/mypage.html', {
        'user_form': user_form,
        'password_form': password_form,
        'address_form': address_form,
        'new_address_form': new_address_form,
        'addresses': addresses,
        'selected_address': selected_address,
        'addresses_json': addresses_json,
    })

# -------------------
# ドロップダウンで住所情報を返す関数
# -------------------
@login_required
def get_address(request, address_id):
    try:
        address = Address.objects.get(id=address_id, user=request.user)
        return JsonResponse({
            'postal_code': address.postal_code,
            'prefecture': address.prefecture,
            'city': address.city,
            'detail': address.detail,
        })
    except Address.DoesNotExist:
        return JsonResponse({'error': '住所が見つかりません'}, status=404)
    
# -------------------
# 住所削除
# -------------------
@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, '住所を削除しました。')
    return redirect('users:mypage')

