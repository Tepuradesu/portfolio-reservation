from django import forms
import datetime
# プルダウンの選択肢
CHOICES = (
    ("1", "1月"),
    ("2", "2月"),
    ("3", "3月"),
    ("4", "4月"),
    ("5", "5月"),
    ("6", "6月"),
    ("7", "7月"),
    ("8", "8月"),
    ("9", "9月"),
    ("10","10月"),
    ("11","11月"),
    ("12","12月"),
)


class AdminMonthSelectForm(forms.Form):    
    pulldown = forms.ChoiceField(
               widget=forms.Select,
               choices=CHOICES,
               label="表示月選択")

class MonthSelectForm(forms.Form):
    """定数リストによるプルダウンメニュー"""
    pulldown = forms.ChoiceField(
               widget=forms.Select,
               label="支払月選択")
     
    def __init__(self,*args,**kwargs):
      super().__init__(*args,**kwargs)
      for field in self.fields.values():
        field.widget.attrs['class'] = "menu-list-form-select-month" 
      
 
class CancelBookingMenu(forms.Form):
    name = forms.CharField(label='名前', max_length=100)
    email = forms.EmailField(label='メール', max_length=100)
