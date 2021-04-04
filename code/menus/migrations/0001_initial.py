# Generated by Django 2.2.16 on 2020-09-21 06:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Menus',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(null=True, verbose_name='提供日')),
                ('staple_food', models.CharField(max_length=50)),
                ('main_dish', models.CharField(max_length=50)),
                ('side_dish', models.CharField(max_length=50)),
                ('soup', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='BookingMenu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reservation_time', models.DateTimeField(verbose_name='予約時間帯')),
                ('menus', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='menus.Menus')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
