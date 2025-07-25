from django import forms
from django.contrib.auth import get_user_model
from users.models import Address, CustomUser
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

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

class CustomLoginForm(AuthenticationForm):
    username = forms.CharField(
        label='ユーザーネーム',
        widget=forms.TextInput(attrs={'autofocus': True})
    )
    password = forms.CharField(
        label='パスワード',
        widget=forms.PasswordInput
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

class PasswordUpdateForm(forms.Form):
    current_password = forms.CharField(label='現在のパスワード', widget=forms.PasswordInput)
    new_password = forms.CharField(label='新しいパスワード', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='新しいパスワード(確認用)',widget=forms.PasswordInput)

    def clean(self):
        cleaned_data = super().clean()
        new_password = cleaned_data.get('new_password')
        confirm_password = cleaned_data.get('confirm_password')

        if new_password and confirm_password and new_password != confirm_password:
            raise forms.ValidationError('新しいパスワードが一致しません。')
        
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