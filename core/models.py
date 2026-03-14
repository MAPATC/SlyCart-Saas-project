from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class TelegramUser(models.Model):
    user_id = models.BigIntegerField(unique=True)

    ROLE_CHOICES = [
        ('customer', 'Покупатель'),
        ('owner', 'Владелец'),
    ]

    role = models.CharField(
        max_length=10,
        choices=ROLE_CHOICES, # Первое для базы(customer), второе для админки(Покупатель)
        default='customer'
    )

    reg_date = models.DateField(auto_now_add=True) #Автодобавление даты регистрации

    def __str__(self):
        return f"{self.user_id} ({self.role})"
    

class Tariff(models.Model):
    plan = models.CharField(max_length=50)
    limits = models.PositiveIntegerField(default=5)
    # max_digit - максимальное количество цифр в числе, decimal_places - знаки после запятой
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Тариф"
        verbose_name_plural = "Тарифы" # Чтобы в админке не было "Тарифs"

    def __str__(self):
        return f'{self.tariff} -> {self.price}:{self.limits} '