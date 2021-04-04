from django.urls import path
from . import views

app_name ='authentication'
urlpatterns = [
     path('signup/', views.SignUp.as_view(), name='signup'),
     path('top/',views.Top.as_view(),name='top'),
     path('signin/', views.SignIn.as_view(), name='signin'),
     path('logout/', views.Logout.as_view(), name='logout'),
     path('temporary_registration/',views.TemporaryRegistration.as_view(),name='temporary_registration'),
     path('complete_registration/<token>', views.CompleteaRegistration.as_view(), name='complete_registration'),
     path('mypage', views.MyPage.as_view(), name='mypage'),
     
]