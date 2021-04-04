from django.contrib import admin
from django.urls import path,include

# 追加
admin.site.site_title = 'タイトルタグ' 
admin.site.site_header = 'めぐろめし。'
admin.site.index_title = 'メニュー'



urlpatterns = [
    path('admin/', admin.site.urls),
    path('authentication/', include('authentication.urls')),
    path('personality/', include('personality.urls')),
    path('menus/', include('menus.urls')),
    path('payment/', include('payment.urls')),
    path('authentication/', include('django.contrib.auth.urls')),
]
