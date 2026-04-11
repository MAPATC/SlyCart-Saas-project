from ninja import Router
from typing import List
from django.shortcuts import get_object_or_404
from .models import TelegramUser, OwnerProfile, Product, Shop
from .services import create_user, create_shop, create_product
from .schemas import (TelegramUserOut, 
                      TelegramUserIn,
                      ShopIn,
                      ShopOut,
                      ProductIn,
                      ProductOut)

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
        name=data.shop_name,
        link=data.shop_link
    )

    return shop

@core_router.post("/product", response=ProductOut)
def create_product_endpoint(request, data: ProductIn):

    shop_obj = get_object_or_404(Shop, id=data.shop, owner__owner__user_id=data.user_id)

    product = create_product(
        shop=shop_obj,
        title=data.title,
        description=data.description,
        price=data.price,
        stock=data.stock,
        is_active=data.is_active
    )

    return product

@core_router.get("/my-shops", response=List[ShopOut])
def list_my_shops(request, user_id: int):

    shops = Shop.objects.filter(owner__owner__user_id=user_id)

    return shops

# TODO: эндпоинт для товаров