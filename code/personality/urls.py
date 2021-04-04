from django.urls import path
from . import views

app_name ='personality'
urlpatterns = [
      path('edit_profile/<int:pk>/', views.EditProfile.as_view(), name='edit_profile'),
]
