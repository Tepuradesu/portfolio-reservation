from django.shortcuts import render
from django.contrib.auth.views import LoginView, LogoutView
from django.views.generic import CreateView,TemplateView,UpdateView
from .forms import SignUpForm,LoginForm
from django.views import generic
from django.urls import reverse_lazy,reverse
from .models import MyUser
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import redirect
from django.contrib.sites.shortcuts import get_current_site
from django.core.signing import BadSignature, SignatureExpired, loads, dumps
import booking.settings
from django.template.loader import get_template
from . import utils
from .forms import SignInForm
from django.contrib.auth.mixins import LoginRequiredMixin



class SignUp(generic.CreateView):
    form_class = SignUpForm
    success_url = reverse_lazy('login')
    template_name = 'authentication/signup.html'
    
    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect((reverse('authentication:mypage')))
        return super().get(request, **kwargs)
    

    def form_valid(self, form):
        # 仮登録
        user = form.save(commit=False)
        user.is_active = False
        user.save()

        # メール送信
        current_site = get_current_site(self.request)
        domain = current_site.domain
        context = {
            'protocol': 'https' if self.request.is_secure() else 'http',
            'domain': domain,
            'token': dumps(user.pk),
            'user': user
        }
        subject_template = get_template('mail/subject.txt')
        message_template = get_template('mail/message.txt')
        subject = subject_template.render(context)
        message = message_template.render(context)

        
        email_from = settings.EMAIL_HOST_USER
        recipient_list=[]
        recipient_list.append('ottitrade@gmail.com')
        html_message=''
        send_mail(subject, message, email_from, recipient_list, html_message=message)
        return redirect('authentication:temporary_registration')

#class Login(LoginView):
#    form_class = LoginForm
#    success_url = 'registration/top.html'
#    template_name = 'registration/login.html'

class Logout(LogoutView):
    template_name = 'authentication/top.html'

class Top(generic.TemplateView):
    template_name = 'authentication/top.html'
    #お試しで追加
    #def get_context_data(self, **kwargs):
    # context = super().get_context_data(**kwargs)
    # context['cookie'] = self.request.COOKIES.get('key')
    
    # return context
    


class TemporaryRegistration(generic.TemplateView):
    """仮登録完了"""
    template_name = 'authentication/temporary_registration.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect((reverse('authentication:top')))
        return super().get(request, **kwargs)


class CompleteaRegistration(generic.TemplateView):
    """本登録完了"""
    template_name = 'authentication/complete_registration.html'
    #アクティベーションURLの有効期限を設定する。
    #60*60*24 =１分X60X24時間
    timeout_seconds = getattr(settings, 'ACTIVATION_TIMEOUT_SECONDS', 60 * 60 * 24)  # デフォルトでは1日以内

    def get(self, request, **kwargs):
        """tokenが正しければ本登録."""
        if request.user.is_authenticated:
            return HttpResponseRedirect((reverse('authentication:top')))
            
        #トークンを復号する。
        token = kwargs.get('token')
        try:
            user_pk = loads(token, max_age=self.timeout_seconds)

        # 期限切れ 1日経過してアクティベーションリンクを踏んだ場合
        except SignatureExpired:
            return HttpResponseBadRequest()

        # tokenが間違っている トークンを適当に入力した場合
        except BadSignature:
            return HttpResponseBadRequest()

        # tokenは問題なし
        try:
            user = MyUser.objects.get(pk=user_pk)
        except MyUser.DoenNotExist:
            return HttpResponseBadRequest()

        if not user.is_active:
            # 問題なければ本登録とする
            user.is_active = True
            user.save()

            # QRコード生成
            request.session["img"] = utils.get_image_b64(utils.get_auth_url(user.email, utils.get_secret(user)))

            return super().get(request, **kwargs)

        return HttpResponseBadRequest()


class SignIn(LoginView):
    """ログイン"""
    form_class = SignInForm
    template_name = 'authentication/signin.html'
    success_url = 'authentication/mypage.html'

    def get(self, request, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect((reverse('authentication:mypage')))
        return super().get(request, **kwargs)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        return context


class MyPage(LoginRequiredMixin,generic.TemplateView):
    login_url = '/authentication/signin/'
    template_name = 'authentication/mypage.html'
    
    def get_context_data(self, **kwargs):
     context = super().get_context_data(**kwargs)
     user_id = self.request.user.id
     user_name = MyUser.objects.get(pk=user_id).email
     context['user_name'] = user_name
     
     return context
