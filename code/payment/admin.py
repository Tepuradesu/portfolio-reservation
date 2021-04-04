from django.contrib import admin
from booking import settings
from authentication.models import MyUser
from .models import Payments
from django.template.response import TemplateResponse
from django.urls import path
import datetime
from .forms import MonthSelectForm

@admin.register(Payments)
class PaymentsAdmin(admin.ModelAdmin):
   #url追加処理
   def get_urls(self):
    urls = super().get_urls()
    add_urls = [
       path('paymentlist/', self.admin_site.admin_view(self.list_view), name="paymentlist"),
       path('paymentdetail/<int:pk>/',self.admin_site.admin_view(self.detail_view), name="paymentdetail"),
    ]
    return add_urls + urls

   def get_payment_queryset(self,year,month):
     #データ基準日を設定する。
     start_day = datetime.datetime(year,month,1,0,0,0,0)
     if month == 12:
       end_day = datetime.datetime(year + 1,1,1,23,0,0,0) - datetime.timedelta(days=1)
     else:
       end_day = datetime.datetime(year,month + 1,1,23,0,0,0) - datetime.timedelta(days=1)
     payment_queryset = Payments.objects.filter(payment_month__gte=start_day,payment_month__lte=end_day)
     
     return payment_queryset

   """
   "機能概要:adminユーザが指定した期間内の支払額をユーザ別に整理してDictionary型データを作る。
   "        :①POSTの場合:pulldownで選択された支払月分のデータを取得する。
   "        :②GETの場合 :今日日付で支払月分のデータを取得する。
   """
   def list_view(self, request,**kwargs):
    today = datetime.date.today()
    year = today.year
    month = today.month
    
    #プルダウンから表示月を選択した時はPOST通信
    if request.method == 'POST':
      form = MonthSelectForm(request.POST)
      if form.is_valid():
         #画面pulldownから支払月を取得する。
         month = int(form.cleaned_data['pulldown'])
         payment_queryset = self.get_payment_queryset(year,month)
    #直接urlを叩いてアクセスした時はGET通信
    if request.method == 'GET':
      payment_queryset = self.get_payment_queryset(year,month)
    	
    payment_list = {}
    initial_dict ={'pulldown':month}
    select_month = MonthSelectForm(request.GET or request.POST,initial=initial_dict)
    payment_list.setdefault('select_month',select_month)
    id_list = [ payment_query.id for payment_query in payment_queryset]

    payment_list.setdefault('user',{})
    for i in id_list:
     payment_quer = Payments.objects.select_related('user').get(id=i)
     #ユーザ名をkeyにして辞書をネストする。
     payment_list['user'].setdefault(payment_quer.user.email,{}) 
     payment_list['user'][payment_quer.user.email].setdefault('meal_expenses',payment_quer.meal_expenses)
     payment_list['user'][payment_quer.user.email].setdefault('other_expenses',payment_quer.other_expenses)
     payment_list['user'][payment_quer.user.email].setdefault('total_expenses',payment_quer.meal_expenses + payment_quer.other_expenses)
     payment_list['user'][payment_quer.user.email].setdefault('is_paid',payment_quer.is_paid)
     payment_list['user'][payment_quer.user.email].setdefault('user_id',payment_quer.user_id)
    return TemplateResponse(request, "admin/payment/payments/paymentlist.html",payment_list)
    
   
   def detail_view(self,request,**kwargs):
    #urlからユーザIDを取得する。
    user_id = kwargs['pk']
    context = {}
    context['user_id'] = user_id
    return TemplateResponse(request, "admin/payment/payments/paymentdetail.html",context)
    

