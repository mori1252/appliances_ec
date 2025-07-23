from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            # else:
                #フォームが無効な場合のエラー処理
        else:
            form = AuthenticationForm()
        return render(request, 'users/login.html', {'form': form})
    
def user_logout(request):
    logout(request)
    return redirect('home')

def user_register(request):
    #ユーザー登録のロジックをここに書く
    return render(request, 'users/register.html')

@login_required #ログインしていないとアクセスできないようにする
def user_profile(request):
    #ユーザープロフィールの表示ロジックをここに書く
    return render(request, 'users/profile.html')