from django.contrib import admin
from .models import TelegramUser, Tariff, CustomerProfile, OwnerProfile, Shop, Product, CartItem, Order, OrderItem, ProductImage

# Register your models here.
admin.site.register(TelegramUser)
admin.site.register(CustomerProfile)
admin.site.register(OwnerProfile)
admin.site.register(Tariff)
admin.site.register(Shop)
admin.site.register(Product)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ProductImage)


