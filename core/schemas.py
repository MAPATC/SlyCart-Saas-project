from ninja import Schema
from datetime import date
from .models import TelegramUser

class TelegramUserIn(Schema): # Что мы будем вносить
    user_id: int
    role: str
    phone_number: str
    inn: str = None
    brand_name: str = None
    

class TelegramUserOut(Schema): # Что мы будем показывать в front
    user_id: int
    role: str