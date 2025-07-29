from django import forms
from django.contrib.auth import get_user_model
from users.models import Address, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordChangeForm

User = get_user_model()

# 新規登録フォーム（ラベル追加）
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'mail_address', 'password1', 'password2')
        labels = {
            'username': 'ユーザーネーム',
            'mail_address': 'メールアドレス',
            'password1': 'パスワード',
            'password2': 'パスワード（確認用）',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'mail_address': forms.EmailInput(attrs={'class': 'form-control text-center'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control text-center'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control text-center'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # password1, password2 のwidget attrsを個別設定
        self.fields['password1'].widget.attrs.update({'class': 'form-control text-center'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control text-center'})

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='ユーザーネーム',
        widget=forms.TextInput(attrs={'class': 'form-control text-center', 'autofocus': True})
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput(attrs={'class': 'form-control text-center'})
    )

# ユーザー情報変更フォーム（ラベル追加）
class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'mail_address']
        labels = {
            'username': 'ユーザーネーム',
            'mail_address': 'メールアドレス',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'mail_address': forms.EmailInput(attrs={'class': 'form-control text-center'}),
        }

# パスワード更新フォーム
class PasswordUpdateForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # ここでラベルやウィジェットのカスタマイズも可能
        self.fields['old_password'].label = "現在のパスワード"
        self.fields['new_password1'].label = "新しいパスワード"
        self.fields['new_password2'].label = "新しいパスワード（確認用）"
        
        for field in self.fields.values():
            field.widget.attrs.update({'class': 'form-control text-center'})


        
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['postal_code', 'prefecture', 'city', 'street', 'building']
        labels = {
            'postal_code': '郵便番号',
            'prefecture': '都道府県',
            'city': '市区町村',
            'street': '番地・丁目',
            'building': '建物名・部屋番号',
        }
        widgets = {
            'postal_code': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'prefecture': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'city': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'street': forms.TextInput(attrs={'class': 'form-control text-center'}),
            'building': forms.TextInput(attrs={'class': 'form-control text-center'}),
        }