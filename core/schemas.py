from ninja import Schema
from datetime import date
from .models import TelegramUser

class TelegramUserIn(Schema):
    user_id: int
    role: str = "customer"


class TelegramUserOut(Schema):
    user_id: int
    role: str
    reg_date: date
