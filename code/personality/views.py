from django.shortcuts import render
from django.views.generic import UpdateView
from .forms import EditProfileForm
from authentication.models import MyUser

class EditProfile(UpdateView):
    model = MyUser
    form_class = EditProfileForm
    template_name = 'personality/edit_profile.html'
    #success_url = reverse_lazy('menus:menulist')
