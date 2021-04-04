from django.db import models
from django.dispatch import receiver
from booking import settings

#支払クラス
class Payments(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    meal_expenses = models.IntegerField(null=True)
    other_expenses = models.IntegerField(null=True)
    payment_deadline = models.DateTimeField('支払締切日',null=True)
    payment_month = models.DateTimeField('支払月',null=True)
    is_paid = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'hogehoge'
        verbose_name_plural = 'カテゴリー'

