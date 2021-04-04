from django.shortcuts import render
from django.views.generic import FormView,ListView,CreateView,UpdateView,DeleteView
from .models import Menus,BookingMenu
from authentication.models import MyUser
from django.db.models import Q
from django.shortcuts import get_object_or_404
import datetime
from django.urls import reverse, reverse_lazy
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from .forms import MonthSelectForm
import pytz
from django.shortcuts import redirect
from urllib.parse import urlencode
from django.contrib.auth.mixins import LoginRequiredMixin

class MenusListView(LoginRequiredMixin,ListView):
     login_url = '/authentication/signin/'
     template_name = 'menus/menu_list.html'
     model = Menus
     
     def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userid = self.request.user.id
        selected_month = self.request.GET.get("pulldown")
        date_today = datetime.date.today()
        year = date_today.year
        month = date_today.month
        day =  date_today.day
        
        context['today'] = date_today
        
        reservation_list = {}
        
        #献立一覧画面で基準月が選択されなかった場合
        #データ基準日を今日日付にする。
        if not selected_month and month != 12:
          start_day = datetime.datetime(year,month,1,0,0,0,0)
          end_day = datetime.date(year,int(month) + 1,1) - datetime.timedelta(days=1)
        elif not selected_month and month == 12:
          start_day = datetime.datetime(year,month,1,0,0,0,0)
          end_day = datetime.datetime(year + 1,1,1,23,0,0,0) - datetime.timedelta(days=1)
        #献立一覧画面で不正月が基準月に選択された場合
        #データ基準日を今日日付にし、エラーメッセージを設定する。
        elif (int(selected_month) > 12 or int(selected_month) < 1) and month != 12:
          context['error_message'] = "指定された月が不正です。"
          start_day = datetime.datetime(year,month,1,0,0,0,0)
          end_day = datetime.date(year,int(month) + 1,1) - datetime.timedelta(days=1)
        elif (int(selected_month) > 12 or int(selected_month) < 1) and month == 12:
          context['error_message'] = "指定された月が不正です。"  
          start_day = datetime.datetime(year,month,1,0,0,0,0)
          end_day = datetime.datetime(year + 1,1,1,23,0,0,0) - datetime.timedelta(days=1)
        elif int(selected_month) == 1 and month == 12:
          start_day = datetime.datetime(year + 1,int(selected_month),1,0,0,0,0)
          end_day = datetime.date(year + 1,int(selected_month) + 1,1) - datetime.timedelta(days=1)
        #12月が選択された場合
        elif int(selected_month) == 12:
          start_day = datetime.datetime(year,int(selected_month),1,0,0,0,0)
          end_day = datetime.datetime(year + 1,1,1,23,0,0,0) - datetime.timedelta(days=1)
        else:
           start_day = datetime.datetime(year,int(selected_month),1,0,0,0,0)
           end_day = datetime.date(year,int(selected_month) + 1,1) - datetime.timedelta(days=1)

        context['start_day']=start_day
        context['end_day'] = end_day

        #献立一覧画面の表示月プルダウンリストを作る。
        select_month = MonthSelectForm()
        if month < 12:
          select_month.fields['pulldown'].choices = ((month,'{0}月'.format(month)),(month+1,'{0}月'.format(month+1)))
        elif month == 12:
          select_month.fields['pulldown'].choices = ((month,'{0}月'.format(month)),(month-11,'{0}月'.format(month-11)))
        context['select_month']=select_month

        #start_dayからend_dayまで30日分の献立情報を取得する。
        menu_queryset = Menus.objects.filter(date__gte=start_day,date__lte=end_day).order_by('date')

        #献立ID一覧をタプル変換して取得する。
        menu_ids = [menu.id for menu in menu_queryset]
        #データ構造
        #reservation_list
        #{menu_id:{'existence':True,'changeable':False}}}
        context.setdefault('reservation_time_limite',[])
        for (menu_id,menu) in zip(menu_ids,menu_queryset):
         reservation = BookingMenu.objects.filter(user_id=userid,menus_id=menu_id)
         reservation_time_limite = datetime.datetime(menu.date.year,menu.date.month,menu.date.day,10, 0, 0, 0)
         context['reservation_time_limite'].append(reservation_time_limite)
         #予約済みの場合
         if not reservation.count() == 0:
           reservation_list.setdefault(menu_id,{})
           reservation_list[menu_id]['existence']=True
         #未予約の場合
         else:
           reservation_list.setdefault(menu_id,{})
           reservation_list[menu_id]['existence']=False
           
         if datetime.datetime.now() <= reservation_time_limite:
          reservation_list[menu_id]['changeable']=True
         else:
          reservation_list[menu_id]['changeable']=False
              
        context.setdefault('menu_list',{}) 
        if not menu_queryset.count() == 0: 
         for (menu,reservation) in zip(menu_queryset,reservation_list.values()):
           context['menu_list'].setdefault(menu.date.strftime('%Y/%m/%d'),\
                         {'id':menu.id,\
                         'staple_food':menu.staple_food,\
                         'main_dish':menu.main_dish,\
                         'side_dish':menu.side_dish,\
                         'soup':menu.soup,\
                         'reservation':reservation['existence'],\
                         'changeable':reservation['changeable']})
        return context
        
class BookinMenuView(LoginRequiredMixin,UpdateView):
     login_url = '/authentication/signin/'

     """
     "機能概要:献立一覧画面で予約チェックを付けたレコードをBookingMenuに新規登録する。
     "        :I(献立一覧画面で予約チェックを付けた献立ID)  self.request.POST.getlist('checks')
     "        :I(ログイン中ユーザID)  self.request.user.id
     """
     def post(self, request, *args, **kwargs):
        #チェックボックスにマークがされた献立のidを取得する。
        check_values = request.POST.getlist('checks')
        #ログイン中のユーザIDを取得する。
        userid = self.request.user.id
        for check_value in check_values:
         #献立提供日を取得する。
         reserve_date = Menus.objects.get(pk=check_value).date
         if not BookingMenu.objects.filter(user_id=userid,menus_id=check_value).exists():
            BookingMenu.objects.create(user_id=userid,menus_id=check_value,reservation_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),date=reserve_date.strftime('%Y-%m-%d %H:%M:%S'))
        redirect_url =reverse('menus:menulist')
        #parameters = urlencode({'pulldown': ''})
        #url = f'{redirect_url}?{parameters}'
        url = f'{redirect_url}'
        return redirect(url)
        
        
        
class CancelBookingMenuView(LoginRequiredMixin,DeleteView):
      login_url = '/authentication/signin/'
      template_name = 'menus/bookingmenu_confirm_delete.html'
      success_url = reverse_lazy('menus:menulist')
      model = BookingMenu
      
      def get_context_data(self, **kwargs):
       context = super().get_context_data(**kwargs)
       #キャンセル後、ブラウザバックされた場合,
       #不正pkがurlに含まれていた場合
       if self.object == "":
        context['submit_flag'] = False
        context['error_message'] = "既にキャンセル済みか、urlに不正な日付が入力されています。" 
       else:
        booking_day = Menus.objects.get(pk=self.kwargs.get(self.pk_url_kwarg)).date.strftime('%Y年%m月%d日')
        context['booking_day'] = booking_day
        context['submit_flag'] = True
       return context
      
      def get_queryset(self):
         #ログイン中のユーザIDを取得する。
         userid = self.request.user.id
         if self.queryset is None:
            if self.model:
             return self.model.objects.filter(user_id =userid)
         else:
            raise ImproperlyConfigured(
                "%(cls)s is missing a QuerySet. Define "
                "%(cls)s.model, %(cls)s.queryset, or override "
                "%(cls)s.get_queryset()." % {
                    'cls': self.__class__.__name__
                }
            )
         return self.queryset.all()

      def get_object(self, queryset=None):
          if queryset is None:
              queryset = self.get_queryset()
      
          pk = self.kwargs.get(self.pk_url_kwarg)
          slug = self.kwargs.get(self.slug_url_kwarg)
          if pk is not None:
              queryset = queryset.filter(menus_id=pk)
          if slug is not None and (pk is None or self.query_pk_and_slug):
              slug_field = self.get_slug_field()
              queryset = queryset.filter(**{slug_field: slug})
          if pk is None and slug is None:
              raise AttributeError(
                  "Generic detail view %s must be called with either an object "
                  "pk or a slug in the URLconf." % self.__class__.__name__
              )
          try:
              if queryset.count() == 1:
                obj = queryset.get()
              else:
                obj = ""
                                
          except queryset.model.DoesNotExist:
              #修正要
              raise Http404(_("No %(verbose_name)s found matching the query") %
                            {'verbose_name': queryset.model._meta.verbose_name})
          return obj