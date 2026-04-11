from decimal import Decimal
from pydantic import PositiveInt
import uuid
from ninja import Schema, ModelSchema
from datetime import date
from .models import TelegramUser, Shop, Product

class TelegramUserIn(Schema): # Что мы будем вносить
    user_id: int
    role: str
    phone_number: str
    inn: str = None
    brand_name: str = None


class TelegramUserOut(ModelSchema): # Что мы будет отдавать в front(modelschema лучше использовать для Out)
    class Meta:
        model = TelegramUser
        fields = ['user_id', 'role']


class ShopIn(Schema):
    owner: int
    shop_name: str
    shop_link: str = None


class ShopOut(ModelSchema):
    # ModelSchema сделает все сама
    owner_id: int  # Это "дополнительное" поле для JSON

    class Meta:
        model = Shop
        fields = ['id', 'shop_name', 'shop_link'] # Здесь ТОЛЬКО реальные колонки из таблицы Shop

    @staticmethod # "Добытчик" сам все найдет и напишет
    def resolve_owner_id(obj):
        return obj.owner.owner.user_id


class ProductIn(Schema):
    shop: uuid.UUID
    user_id: int
    title: str
    description: str
    price: Decimal
    stock: PositiveInt
    is_active: bool = True


class ProductOut(ModelSchema):
    class Meta:
        model = Product
        fields = ["title", "description", "price", "stock", "is_active"]
