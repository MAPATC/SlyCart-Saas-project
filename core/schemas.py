import uuid
from ninja import Schema, ModelSchema
from datetime import date
from .models import TelegramUser, Shop

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
    shop_link: str = None


class ShopOut(ModelSchema):
    class Meta:
        model = Shop
        fields = ['id', 'owner','shop_name', 'shop_link']
