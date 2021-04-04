from django.urls import path
from . import views

app_name ='menus'
urlpatterns = [
      path('listmenu/',views.MenusListView.as_view(),name='menulist'),
      path('bookingmenu/', views.BookinMenuView.as_view(), name='booking_menu'),
      path('cancel_bookingmenu/<int:pk>/', views.CancelBookingMenuView.as_view(), name='cancel_booking_menu'),
]
