# Generated by Django 3.1 on 2021-02-13 16:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('menus', '0002_bookingmenu_date'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='menus',
            options={'verbose_name_plural': '献立'},
        ),
        migrations.AlterField(
            model_name='menus',
            name='main_dish',
            field=models.CharField(max_length=50, verbose_name='主菜'),
        ),
        migrations.AlterField(
            model_name='menus',
            name='side_dish',
            field=models.CharField(max_length=50, verbose_name='副菜'),
        ),
        migrations.AlterField(
            model_name='menus',
            name='soup',
            field=models.CharField(max_length=50, verbose_name='汁物'),
        ),
        migrations.AlterField(
            model_name='menus',
            name='staple_food',
            field=models.CharField(max_length=50, verbose_name='主食'),
        ),
    ]