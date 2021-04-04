from django.shortcuts import render
from django.views.generic import TemplateView,FormView,DetailView
from menus.models import Menus,BookingMenu
from authentication.models import MyUser
import datetime,calendar
from datetime import datetime,timedelta
import datetime
from django.contrib.auth.mixins import LoginRequiredMixin

class PaymentView(LoginRequiredMixin,TemplateView):
    login_url = '/authentication/signin/'
    template_name = 'payment/top.html'
    MEAL_EXPENSES = 500
   
    def get_context_data(self, **kwargs):
      context = super().get_context_data(**kwargs)
      user_id = self.request.user.id
      context['email'] = MyUser.objects.values_list('email',flat=True).get(pk=user_id)
      
      #当月支払い予定額を計算する。
      #年取得
      today = datetime.datetime.today()
      current_year = today.year
      current_month = today.month
      context['current_year'] = current_year
      
      if current_month == 1:
       last_month = 12
      else:
       last_month = current_month -1
      
      context['last_month'] = last_month
      #先月の情報を取得
      _, last_month_last_day = calendar.monthrange(current_year,last_month)
      #当月の情報を取得
      current_month_first_day = (datetime.date(current_year,last_month,last_month_last_day) + datetime.timedelta(days=1)).day
      _, current_month_last_day = calendar.monthrange(current_year,current_month)
      context['current_month_last_day'] = current_month_last_day
      context['current_month_first_day'] = current_month_first_day
      context['current_month'] = current_month
      context['today'] = today
      
      #食事回数計算処理
      #当月1日から当月最終日まで献立予約回数を基に計算する。
      #当月初日
      start_day = datetime.date(current_year,current_month,current_month_first_day)
      #当月最終日
      end_day = datetime.date(current_year,current_month,current_month_last_day)
      #計算期間内の献立idをリスト形式で取得
      list_menu_id = Menus.objects.filter(date__gte=start_day,date__lte=end_day).values_list('id',flat = True)
      #食事回数を算出する。
      reservation_times = BookingMenu.objects.filter(user_id=user_id,menus_id__in=list_menu_id).count()
      #テレビ設置代金とかは後ほど追記する。
      if reservation_times != 0:
         payment = reservation_times * self.MEAL_EXPENSES
      else:
         payment = 0
      context['payment'] = payment
      return context
  
