from django import forms
from django.contrib.auth import get_user_model
from users.models import Address, CustomUser
from django.contrib.auth.forms import UserCreationForm

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'mail_address', 'password1', 'password2')

class UserUpdateForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'mail_address']

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
    set_as_default = forms.BooleanField(required=False, label='デフォルト配送先に設定')

    class Meta:
        model = Address
        fields = ['postal_code', 'prefecture', 'street', 'building']