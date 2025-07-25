from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cart.models import Cart, CartItem
from .models import Address
from .forms import UserUpdateForm, PasswordUpdateForm, AddressForm, CustomUserCreationForm, CustomLoginForm




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

    # デフォルト住所を取得（なければNone）
    default_address = addresses.filter(is_default=True).first()

    if request.method == 'POST':
        if 'update_user' in request.POST:
            user_form = UserUpdateForm(request.POST, instance=user)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'ユーザー情報を更新しました。')
                return redirect('users:mypage')
            else:
                messages.error(request, 'ユーザー情報の更新に失敗しました。')

        elif 'update_password' in request.POST:
            password_form = PasswordUpdateForm(user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                update_session_auth_hash(request, user)  # セッション維持
                messages.success(request, 'パスワードを更新しました。')
                return redirect('users:mypage')
            else:
                messages.error(request, 'パスワードの更新に失敗しました。')

        elif 'add_address' in request.POST:
            user_form = UserUpdateForm(instance=user)
            password_form = PasswordUpdateForm()
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                # 住所追加とデフォルト切替処理
                address = address_form.save(commit=False)
                address.user = user

                if address_form.cleaned_data.get('set_as_default'):
                    # 既存のデフォルト住所を解除
                    Address.objects.filter(user=user, is_default=True).update(is_default=False)
                    address.is_default = True

                address.save()
                messages.success(request, '住所を追加しました。')
                return redirect('users:mypage')
            else:
                messages.error(request, '住所の追加に失敗しました。')

        elif 'change_default' in request.POST:
            user_form = UserUpdateForm(instance=user)
            password_form = PasswordUpdateForm()
            address_form = AddressForm()
            default_address_id = request.POST.get('default_address_id')
            if default_address_id:
                # 既存のデフォルト解除
                Address.objects.filter(user=user, is_default=True).update(is_default=False)
                # 新たに指定された住所をデフォルトに設定
                Address.objects.filter(id=default_address_id, user=user).update(is_default=True)
                messages.success(request, 'デフォルト配送先を変更しました。')
                return redirect('users:mypage')
            else:
                messages.error(request, 'デフォルト配送先の変更に失敗しました。')
    else:
        user_form = UserUpdateForm(instance=user)
        password_form = PasswordUpdateForm()
        address_form = AddressForm()

        # 住所フォームの初期値セット
        if default_address:
            address_form = AddressForm(instance=default_address)
        else:
            address_form = AddressForm()

    return render(request, 'users/mypage.html', {
        'user_form': user_form,
        'password_form': password_form,
        'address_form': address_form,
        'addresses': addresses
    })

# -------------------
# 住所削除
# -------------------
@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, '住所を削除しました。')
    return redirect('users:mypage')
