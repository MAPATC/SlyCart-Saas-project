from django.db import models


# Create your models here.
class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True, verbose_name="ID телеграмм пользователя")

    ROLE_CHOICES = [
        ('customer', 'Покупатель'),
        ('owner', 'Владелец'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES, # Первое для базы(customer), второе для админки(Покупатель)
        default='customer',
        verbose_name="Роль"
    )

    reg_date = models.DateField(auto_now_add=True) #Автодобавление даты регистрации


    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи" 
    
    def __str__(self):
        return f"Пользователь: {self.user_id} ({self.role})"
    

class Tariff(models.Model):
    plan = models.CharField(max_length=50, verbose_name="Тариф")
    limits = models.PositiveIntegerField(verbose_name="Лимиты")
    # max_digit - максимальное количество цифр в числе, decimal_places - знаки после запятой
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена тарифа")
    description = models.TextField(verbose_name="Описание тарифа", blank=True, null=True)
    # blank позволяет быть полю пустым, а null будет сохранять пустые значение как NULL

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы" # Чтобы в админке не было "Тарифs"

    def __str__(self):
        return f'Тариф: {self.plan} -> Цена: {self.price}₽, Лимит: {self.limits} '
    
    
class Shop(models.Model):
    owner = models.ForeignKey(TelegramUser, on_delete=models.CASCADE, verbose_name="Владелец") # Если удалим владельца, удалиться вся информация о магазине(CASCADE)
    # Все о пользователе(тариф, дата регистрации, телеграм айди и т.д)
    # on_delete работает на тех, на кого мы ссылаемся
    tariff = models.ForeignKey(Tariff, on_delete=models.SET_NULL, null=True, verbose_name="Тариф") # Если удалим тариф, то просто поставим NULL в колонке тарифа
    # Все о тарифах
    shop_name = models.CharField(max_length=100, verbose_name="Название магазина")
    shop_link = models.SlugField(unique=True, verbose_name="Ссылка (slug)")


    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        
    def __str__(self):
        return f"Владелец/тариф: {self.owner.user_id} : {self.tariff} (Магазин: {self.shop_name}, link = {self.shop_link})"
    
class Product(models.Model):
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    # Если удалят магазин, вся информация о продуктах тоже удалиться
    title = models.CharField(max_length=100, verbose_name="Название товара")
    description = models.TextField(verbose_name="Описание товара")
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Цена товара")
    is_active = models.BooleanField(verbose_name="Доступен ли товар", default=True)
    stock = models.PositiveIntegerField(verbose_name="Осталось товара", default=1)

    class Meta:
        verbose_name = "Товар"
        verbose_name_plural = "Товары"
        indexes = [
            models.Index(fields=["is_active"], name="goods_in_stock_idx"),
            models.Index(fields=["shop", "price"], name="sorted_prices_idx")
            # В name нельзя ставить пробелы, так как это технические имена
            # Индексы нужны для оптимизации запросов, без индексов базе данных приходиться перебирать все
            # Можно было бы поставить в поля db_index=True, но этот вариант лучше
        ]

    def __str__(self):
        return f"Товар/цена/кол-во: {self.title} : {self.price} : {self.stock}. В наличии: {self.is_active}"