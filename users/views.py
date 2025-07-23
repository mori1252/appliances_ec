from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
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
            else:
                # フォームが無効な場合のエラー処理
                form.add_error(None, 'ユーザー名またはパスワードが正しくありません。')
    else:
        # GETリクエストの場合、空のフォームを表示
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})
    
def user_logout(request):
    logout(request)
    return redirect('products:list')

def user_register(request):
    #ユーザー登録のロジックをここに書く
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save() #ユーザーを保存
            login(request, user) #登録後すぐにログインさせる場合（任意）
            return redirect('products:list')
    else:
        #GETリクエストの場合、空のフォームを表示
        form = UserCreationForm()
    return render(request, 'users/register.html', {'form': form})

@login_required #ログインしていないとアクセスできないようにする
def user_mypage(request):
    #ユーザープロフィールの表示ロジックをここに書く
    return render(request, 'users/mypage.html')