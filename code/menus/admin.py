from django.contrib import admin
from .models import Menus,BookingMenu
from authentication.models import MyUser
from django.template.response import TemplateResponse
from django.urls import path
import datetime
from .forms import AdminMonthSelectForm


#Register your models here.
#admin.site.register(BookingMenu)

@admin.register(BookingMenu)
class BookingMenuAdmin(admin.ModelAdmin):
   #url追加処理
   def get_urls(self):
    urls = super().get_urls()
    add_urls = [
       path('booking_menu_list/', self.admin_site.admin_view(self.booking_menu_list_view), name="booking_menu_list"),
    ]
    return add_urls + urls
    
   def booking_menu_list_view(self,request,**kwargs):
    if request.method == 'GET':
      month = datetime.date.today().month
    elif request.method == 'POST':
      form = AdminMonthSelectForm(request.POST)
      if form.is_valid():
         #画面pulldownから表示月を取得する。
         month = int(form.cleaned_data['pulldown'])
         
    #GET,POST共通処理
    booking_menu_list = {}
    year = datetime.datetime.today().year
    #データ基準日を設定する。
    start_day = datetime.datetime(year,month,1,0,0,0,0)
    if month != 12:     
     end_day = datetime.datetime(year,int(month) + 1,1) - datetime.timedelta(days=1)
    else:
     end_day = datetime.datetime(year + 1,1,1,23,0,0,0) - datetime.timedelta(days=1)    
    
    initial_dict ={'pulldown':month}
    form = AdminMonthSelectForm(request.GET or request.POST,initial=initial_dict)
    booking_menu_list = {}
    booking_menu_list.setdefault('form',form)
    booking_menu_list['start_day'] = start_day.strftime('%Y年%m月%d日')
    booking_menu_list['end_day'] = end_day.strftime('%Y年%m月%d日')
    booking_menu_list.setdefault('day',{})
    booking_menu_queryset = BookingMenu.objects.select_related('user').select_related('menus').filter(reservation_time__gte=start_day,reservation_time__lte=end_day).order_by("date")
    #予約が入っている日付をリスト形式で取得する。
    day_list = [str(queryset.date.day) for queryset in booking_menu_queryset]
    day_list_temp = list(set(day_list))
    day_list_temp.sort()
    day_list = day_list_temp

    for reserve_day in day_list:
     booking_menu_query = booking_menu_queryset.filter(date__year="2021",date__month="1",date__day=reserve_day)
     booking_menu_list['day'].setdefault(reserve_day,[])
     for obj in booking_menu_query:
      booking_menu_list['day'][reserve_day].append(obj.user.email)

    return TemplateResponse(request, "admin/menus/booking/booking_menu_list.html",booking_menu_list)



class MenusAdmin(admin.ModelAdmin):
    list_display = ('date','staple_food','main_dish','side_dish','soup')

admin.site.register(Menus,MenusAdmin)
