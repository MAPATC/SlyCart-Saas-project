from ninja import Router
from django.shortcuts import get_object_or_404
from .models import TelegramUser, OwnerProfile
from .services import create_user, create_shop
from .schemas import (TelegramUserOut, 
                      TelegramUserIn,
                      ShopIn,
                      ShopOut)

core_router = Router()

# Эндпоинты (Endpoints) — это, по сути, «адреса», 
# по которым твой фронтенд (или Telegram-бот) будет обращаться к твоему бэкенду за данными.

@core_router.post("/register", response=TelegramUserOut) # Что то похожее на эндпоинт
def create_user_endpoint(request, data: TelegramUserIn): # Что будет принимать функция

    user = create_user(
        telegram_id=data.user_id,
        role=data.role,
        phone_number=data.phone_number,
        inn=data.inn,
        brand_name=data.brand_name,
        )

    return user
    

@core_router.post('/shop', response=ShopOut)
def create_shop_endpoint(request, data: ShopIn):

    owner = get_object_or_404(OwnerProfile, owner__user_id=data.owner)

    shop = create_shop(
        user=owner,
        link=data.shop_link
    )

    return shop


# TODO: эндпоинт для товаров