from django.urls import path
from . import admin
from . import views

app_name ='payment'
urlpatterns = [     
     path('top/', views.PaymentView.as_view(), name='top'),
]