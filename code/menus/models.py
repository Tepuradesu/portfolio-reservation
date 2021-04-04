from django.db import models
from django.dispatch import receiver
from booking import settings

#献立クラス
class Menus(models.Model):
    date = models.DateTimeField('提供日',null=True)
    staple_food = models.CharField('主食',max_length=50)
    main_dish = models.CharField('主菜',max_length=50)
    side_dish = models.CharField('副菜',max_length=50)
    soup = models.CharField('汁物',max_length=50)
    
    def __str__(self):
        return self.staple_food
        
    class Meta:
        verbose_name_plural = '献立'
#献立予約クラス
class BookingMenu(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    menus = models.ForeignKey(Menus,on_delete=models.CASCADE)
    reservation_time = models.DateTimeField('予約時間帯')
    date = models.DateTimeField('提供日',null=True)
