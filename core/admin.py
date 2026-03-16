from django.contrib import admin
from .models import TelegramUser, Tariff, Shop, Product

# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(Tariff)
admin.site.register(Shop)
admin.site.register(Product)