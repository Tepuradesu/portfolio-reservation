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

class MonthSelectForm(forms.Form):
    """定数リストによるプルダウンメニュー"""
    pulldown = forms.ChoiceField(
               widget=forms.Select,
               choices=CHOICES,
               label="支払月選択")