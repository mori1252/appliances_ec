from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import CustomUser, Address
from .forms import UserUpdateForm, PasswordUpdateForm, AddressForm, CustomUserCreationForm

# ログインビュー
def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, "ログインしました。")
            return redirect('products:list')
        else:
            messages.error(request, "ユーザー名またはパスワードが正しくありません。")
    else:
        form = AuthenticationForm()
    return render(request, 'users/login.html', {'form': form})

#ログアウトビュー
def user_logout(request):
    logout(request)
    messages.success(request, "ログアウトしました。")
    return redirect('products:list')

#登録ビュー
def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        address_form = AddressForm(request.POST)
        if form.is_valid() and (not request.POST.get('register_address') or address_form.is_valid()):
            user = form.save()
            login(request, user)

            # 最初の住所登録（任意）
            if request.POST.get('register_address'):
                address = address_form.save(commit=False)
                address.user = user
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

# マイページ（ログインユーザー専用）
@login_required
def user_mypage(request):
    user = request.user
    addresses = Address.objects.filter(user=user)

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
                update_session_auth_hash(request, user) # ログアウトされないように
                messages.success(request, 'パスワードを更新しました。')
                return redirect('users:mypage')
            else:
                messages.error(request, 'パスワードの更新に失敗しました。')

        elif 'add_address' in request.POST:
            address_form = AddressForm(request.POST)
            if address_form.is_valid():
                address = address_form.save(commit=False)
                address.user =user
                address.save()
                messages.success(request, '住所を追加しました。')
            else:
                messages.error(request, '住所の追加に失敗しました。')
    else:
        user_form = UserUpdateForm(instance=user)
        password_form = PasswordUpdateForm(user)
        address_form = AddressForm()

    return render(request, 'users/mypage.html', {
        'user_form': user_form,
        'password_form': password_form,
        'address_form': address_form,
        'addresses': addresses
        })

# 住所削除
@login_required
def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)
    address.delete()
    messages.success(request, '住所を削除しました。')
    return redirect('users:mypage')
