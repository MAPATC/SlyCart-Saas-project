from rest_framework.serializers import ModelSerializer
from .models import TelegramUser, Tariff, Shop, Product, CartItem, Order, OrderItem
#  Лучше сначала импортировать "инструменты", а потом свои файлы


class TelegramUserSerializer(ModelSerializer):
    # Можно было бы использовать HyperlinkedModelSerializer для RESTful, 
    # но для меня это лишняя нагрузка
    class Meta:
        model = TelegramUser
        fields = [
            "id", # Айди для удобства в React
            "user_id",
            "role",
            "reg_date"
        ]


class TariffSerializer(ModelSerializer):
    class Meta:
        model = Tariff
        fields = [
            "id",
            "plan",
            "limits",
            "price",
            "description"
        ]


class ShopSerializer(ModelSerializer):
    class Meta:
        model = Shop
        fields = [
            "id",
            "owner",
            "tariff",
            "shop_name",
            "shop_link"
        ]


class ProductSerializer(ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "shop",
            "title",
            "description",
            "price",
            "is_active",
            "stock"
        ]


class CartItemSerializer(ModelSerializer):
    class Meta: 
        model = CartItem
        fields = [
            "id",
            "customer",
            "product",
            "updated_at",
            "quantity"
        ]


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = [
            "id",
            "customer",
            "shop",
            "total_price",
            "status"
        ]


class OrderItemSerializer(ModelSerializer):
    class Meta:
        model = OrderItem
        fields = [
            "id",
            "order",
            "product",
            "product_name",
            "quantity",
            "price_per_item"
        ]