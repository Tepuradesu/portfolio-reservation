from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm
#アクティブになっているユーザモデルを使用できる。
User = get_user_model()
from datetime import datetime
from .models import MyUser
from . import utils


class SignUpForm(UserCreationForm):
    #パスワード入力。
    password1 = forms.CharField(label='パスワード', widget=forms.PasswordInput)
    #確認用パスワード入力。
    password2 = forms.CharField(
        label='確認用パスワード', widget=forms.PasswordInput)

    class Meta:
         model = User
         fields = ('email','date_of_birth','room_number','password1','password2')
         labels = {'email': 'メールアドレス','date_of_birth':'生年月日','room_number': '部屋番号','password1':'パスワード','password2':'確認用パスワード'}
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
         
         
class SignInForm(AuthenticationForm):
    """カスタムログインフォーム"""
    username= forms.CharField(max_length=254,label="メールアドレス")
    token = forms.CharField(max_length=254, label="Microsoft Authenticator OTP")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            field.widget.attrs['class'] = 'form-control'
            #field.widget.attrs['placeholder'] = field.label
    #2段階認証要素チェック
    def confirm_login_allowed(self, user):
        if utils.get_token(user) != self.cleaned_data.get('token'):
            raise forms.ValidationError(
                "'Microsoft Authenticator OTP' is invalid."
            )
        super().confirm_login_allowed(user)


        
class LoginForm(AuthenticationForm):
    #パスワード入力。
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput)
