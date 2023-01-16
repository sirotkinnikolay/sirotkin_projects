from django.contrib.auth.models import User
from django.db import models
import datetime


class Profit(models.Model):
    profit = models.IntegerField(default=0, verbose_name='прибыль')


class CategoryModel(models.Model):
    """Модель категории товаров"""
    group = models.CharField(default='без группы', max_length=100, verbose_name='группа товара')

    def __str__(self):
        return self.group


class ProductModel(models.Model):
    """Модель товара"""
    group_product = models.ForeignKey('CategoryModel', default=None, on_delete=models.CASCADE,
                                      verbose_name='категория товара')
    products = models.CharField(max_length=10000, verbose_name='товар')
    article = models.CharField(default=' ', max_length=100, verbose_name='артикул')
    create_at = models.CharField(default=datetime.datetime.now().date(), max_length=30,  verbose_name='дата добавления')
    comment = models.CharField(default=' ', max_length=100, verbose_name='описание')
    price_zakupka = models.IntegerField(default=0, verbose_name='цена закупочная')
    price = models.IntegerField(default=0, verbose_name='цена')
    spd_count = models.IntegerField(default=0, verbose_name='колличество СПБ')
    mos_count = models.IntegerField(default=0, verbose_name='колличество МОСКВА')
    file = models.FileField(default=None, upload_to='files/')

    @classmethod
    def from_db(cls, db, field_names, values):
        """Методы для отслеживания изменений в поле формы,
         при изменении вычисляется разница значений и записывается в БД"""
        instance = super().from_db(db, field_names, values)
        instance._loaded_values = dict(zip(field_names, values))
        return instance

    def save(self, *args, **kwargs):
        if not self._state.adding:
            new_val_spb = self.spd_count
            old_val_spb = self._loaded_values['spd_count']
            new_val_msk = self.mos_count
            old_val_msk = self._loaded_values['mos_count']
            profit = self._loaded_values['price'] - self._loaded_values['price_zakupka']
            if old_val_spb != new_val_spb:
                if new_val_spb < old_val_spb:
                    total_profit = (old_val_spb - new_val_spb) * profit
                    one = Profit.objects.first()
                    one.profit += total_profit
                    one.save()
            elif old_val_msk != new_val_msk:
                if new_val_msk < old_val_msk:
                    total_profit = (old_val_msk - new_val_msk) * profit
                    one = Profit.objects.first()
                    one.profit += total_profit
                    one.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.products
