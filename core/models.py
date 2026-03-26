from django.db import models


# Create your models here.
class TelegramUser(models.Model):

    user_id = models.BigIntegerField(unique=True, 
                                     verbose_name="ID телеграмм пользователя")

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

    plan = models.CharField(max_length=50, 
                            verbose_name="Тариф")
    limits = models.PositiveIntegerField(verbose_name="Лимиты")

    # max_digit - максимальное количество цифр в числе, decimal_places - знаки после запятой
    price = models.DecimalField(max_digits=10,
                                decimal_places=2, 
                                verbose_name="Цена тарифа")
    
    description = models.TextField(verbose_name="Описание тарифа", 
                                   blank=True, 
                                   null=True)
    # blank позволяет быть полю пустым, а null будет сохранять пустые значение как NULL

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы" # Чтобы в админке не было "Тарифs"

    def __str__(self):
        return f'Тариф: {self.plan} -> Цена: {self.price}₽, Лимит: {self.limits} '
    
    
class Shop(models.Model):

    owner = models.ForeignKey(TelegramUser, 
                              on_delete=models.CASCADE, 
                              verbose_name="Владелец") # Если удалим владельца, удалиться вся информация о магазине(CASCADE)
    # Все о пользователе(тариф, дата регистрации, телеграм айди и т.д)
    # on_delete работает на тех, на кого мы ссылаемся
    tariff = models.ForeignKey(Tariff, 
                               on_delete=models.SET_NULL, 
                               null=True, 
                               verbose_name="Тариф") # Если удалим тариф, то просто поставим NULL в колонке тарифа
    # Все о тарифах
    shop_name = models.CharField(max_length=100,
                                 verbose_name="Название магазина")
    
    shop_link = models.SlugField(unique=True, 
                                 verbose_name="Ссылка (slug)")


    class Meta:
        verbose_name = "Магазин"
        verbose_name_plural = "Магазины"
        
    def __str__(self):
        return f"Владелец/тариф: {self.owner.user_id} : {self.tariff} (Магазин: {self.shop_name}, link = {self.shop_link})"
    
class Product(models.Model):
    
    shop = models.ForeignKey(Shop, 
                             on_delete=models.CASCADE)
    # Если удалят магазин, вся информация о продуктах тоже удалиться
    title = models.CharField(max_length=100, 
                             verbose_name="Название товара")
    
    description = models.TextField(verbose_name="Описание товара")

    price = models.DecimalField(max_digits=10, 
                                decimal_places=2, 
                                verbose_name="Цена товара")
    
    created_at = models.DateTimeField(auto_now_add=True, 
                                      null=True)
    
    is_active = models.BooleanField(verbose_name="Доступен ли товар", 
                                    default=True)
    
    stock = models.PositiveIntegerField(verbose_name="Осталось товара", 
                                        default=1)

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


class CartItem(models.Model):

    customer = models.ForeignKey(TelegramUser, 
                                 on_delete=models.CASCADE, 
                                 verbose_name="Покупатель")
    
    product = models.ForeignKey(Product, 
                                on_delete=models.CASCADE, 
                                verbose_name="Товар")
    
    updated_at = models.DateTimeField(auto_now=True, 
                                      verbose_name="Дата изменения заказа")
    
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество товара")


    class Meta:
        verbose_name = "Корзина"
        verbose_name_plural = "Корзины"
    
    def __str__(self):
        return f"Покупатель {self.customer}, товар: {self.product}, кол-во: {self.quantity}"


class Order(models.Model):

    customer = models.ForeignKey(TelegramUser, 
                                 on_delete=models.CASCADE, 
                                 verbose_name="Покупатель")
    shop = models.ForeignKey(Shop, 
                             on_delete=models.CASCADE, 
                             verbose_name="Магазин")
    
    total_price = models.DecimalField(max_digits=10, 
                                      decimal_places=2, 
                                      verbose_name="Общая цена", 
                                      default=0)

    CHOICES = [
        ("pending", "Ожидает оплаты"),
        ("paid", "Оплачен"),
        ("shipped", "Отправлен"),
        ("completed", "Завершен"),
        ("canceled", "Отменен"),
    ]

    status = models.CharField(max_length=20, 
                              choices=CHOICES, 
                              default='pending', 
                              verbose_name="Статус товара")

    
    class Meta:
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"

    def __str__(self):
        return f"Покупатель: {self.customer}, магазин: {self.shop.shop_name}, к оплате: {self.total_price}, статус: {self.status}"
    


class OrderItem(models.Model):

    order = models.ForeignKey(Order, 
                              on_delete=models.CASCADE, 
                              verbose_name="Заказ", 
                              related_name="items") 
    # Если удалиться заказ, то следовательно нужно и удалить товары в нем
    product = models.ForeignKey(Product, 
                                on_delete=models.SET_NULL, 
                                verbose_name="Товар",
                                null=True,
                                blank=True)
    # Если уберут товар, то просто оставим так, что товара нет, но тогда строчка с товаром останется пустой
    # Значит, ее нужно сохранить
    product_name = models.CharField(verbose_name="Товар(сохранненый)", 
                                    max_length=255, 
                                    null=False)
    # Сохраняем сюда название товара
    quantity = models.PositiveSmallIntegerField(verbose_name="Количество товаров в заказе")
    # Сохраняем количество товара из корзины сюда
    price_per_item = models.DecimalField(verbose_name="Цена за штуку", 
                                         max_digits=10, 
                                         decimal_places=2)
    # Цена за штуку, чтобы легче было считать

    class Meta:
        verbose_name = "Товар в заказе"
        verbose_name_plural = "Заказы с товарами"

    def __str__(self):
        return f"Номер заказа: {self.order_id}, кол-во: {self.quantity}, цена за штуку: {self.price_per_item}"


class ProductImage(models.Model):
    
    product = models.ForeignKey(Product, 
                                on_delete=models.CASCADE, 
                                related_name="images",
                                verbose_name="Товар")
    
    image = models.ImageField(verbose_name="Изображение", 
                                upload_to="products/gallery/%Y/%m/%d/",
                                )
    
    is_main = models.BooleanField(verbose_name="Главное изображение",
                                  default=False)
    
    def save(self, *args, **kwargs):
        # 1) Применяем фильтр для конкретного товара
        other_images = ProductImage.objects.filter(product=self.product)

        if self.id: # Если текущая запись есть, то исключаем ее(для корректного сохранения главного фото)
            other_images = other_images.exclude(id=self.id)
        # Теперь у нас есть конкретный товар магазина (self.id - определенная запись в базе данных)

        # 2) Ставим для первой True 
        if not other_images.exists():
            self.is_main = True

        # 3) Если галочек вообще нигде нет
        elif not self.is_main and not other_images.filter(is_main=True).exists():
            self.is_main = True

        # 4) Если мы хотим изменить главную
        if self.is_main:
            if self.id: # Проверяем есть ли оно в бд
                other_images.exclude(id=self.id).update(is_main = False)
            else: # Если его нет
                other_images.update(is_main=False) # то ставим всем False


        return super().save(*args, **kwargs)
    
    def delete(self, *args, **kwargs):
        # 1) Удаляем фотографию из папки

        if self.image: # Проверяем на случай того, если фотографии нет в папках
            self.image.delete(save=False)

        # 2) Записываем ту, которую удаляем
        was_main = self.is_main
        product = self.product # Записываем товар

        # Делаем удаление
        super().delete(*args, **kwargs)

        # 3) Проверяем, было ли это фото главное
        if was_main:
            # 4) Если было главное, то назначаем первое фото главным
            next_image = ProductImage.objects.filter(product=product).first()
            if next_image: # есть ли еще в базе данных фотографии
                next_image.is_main = True
                next_image.save()

    
    class Meta:
        verbose_name = "Изображение товара"
        verbose_name_plural = "Изображения товаров"

    def __str__(self):
        return f"Фото для {self.product.title} {'(Главное)' if self.is_main else ''}"