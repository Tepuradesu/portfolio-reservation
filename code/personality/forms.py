from django import forms
from django.contrib.auth import get_user_model
#アクティブになっているユーザモデルを使用できる。
User = get_user_model()
from datetime import datetime
from authentication.models import MyUser

class EditProfileForm(forms.ModelForm):
    class Meta:
      model = MyUser
      fields = ('date_of_birth','name','having_tv')
      labels = {'date_of_birth':'生年月日','name':'名前','having_tv':'テレビを持っている'}
      help_texts = {'name':'他のユーザからは見えません。','having_tv':'テレビを持っている場合毎月支払いに計上します。'}
    
    
    
