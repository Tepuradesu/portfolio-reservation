from django import template

register = template.Library() # Djangoのテンプレートタグライブラリ

# カスタムフィルタとして登録する
@register.filter
def convert(dict,key,default=""):
    if key in dict:
     return dict[key]
    else:
     return default
