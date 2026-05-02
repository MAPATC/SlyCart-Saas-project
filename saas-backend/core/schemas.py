from decimal import Decimal
from typing import Optional
from pydantic import PositiveInt
import uuid
from ninja import Field, Schema, ModelSchema
from datetime import date
from .models import TelegramUser, Shop, Product
from enum import Enum

class Roles(str, Enum):
    customer: str
    owner: str

class TelegramUserIn(Schema): # Что мы будем вносить
    user_id: int
    role: Roles
    phone_number: str
    inn: str | None = None
    brand_name: str | None = None


class TelegramUserOut(ModelSchema): # Что мы будет отдавать в front(modelSchema лучше использовать для Out)
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
    price: Decimal = Field(..., max_digits=10, decimal_places=2) # ...(элипс) означает что поле обязательное. 
    # Информацию обязательно должен прислать бекэнд или пользователь 
    stock: PositiveInt
    is_active: bool = True


class ProductOut(ModelSchema):

    price: Decimal = Field(..., max_digits=12, decimal_places=2, json_schema_extra={"example": "0.00"})

    shop_id: uuid.UUID = Field(..., alias="shop.id")

    class Meta:
        model = Product
        fields = ["id", "title", "description", "price", "stock", "is_active"]

class ProductPatch(Schema):
    user_id: int
    title: Optional[str]
    description: Optional[str]
    price: Optional[Decimal] 
    stock: Optional[PositiveInt]
    is_active: Optional[bool]
