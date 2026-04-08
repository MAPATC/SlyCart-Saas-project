from ninja import Schema, ModelSchema
from datetime import date
from .models import TelegramUser

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