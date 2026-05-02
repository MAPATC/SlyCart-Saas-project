import uuid
from ninja import Router, File
from ninja.pagination import paginate
from ninja.files import UploadedFile
from typing import List
from django.shortcuts import get_object_or_404

from .exceptions import NegativePriceError
from .models import TelegramUser, OwnerProfile, Product, Shop
from .services import create_user, create_shop, create_product
from .schemas import (
    TelegramUserOut, 
    TelegramUserIn,
    ShopIn,
    ShopOut,
    ProductIn,
    ProductOut,
    ProductPatch
    )

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

    owner = get_object_or_404(
        OwnerProfile, 
        owner__user_id=data.owner
        )

    shop = create_shop(
        user=owner,
        name=data.shop_name,
        link=data.shop_link
    )

    return shop

@core_router.post("/product", response=ProductOut)
def create_product_endpoint(request, data: ProductIn, images: List[UploadedFile] = File()):

    shop_obj = get_object_or_404(
        Shop, 
        id=data.shop, 
        owner__owner__user_id=data.user_id
        )

    product = create_product(
        shop=shop_obj,
        title=data.title,
        description=data.description,
        images=images,
        price=data.price,
        stock=data.stock,
        is_active=data.is_active
    )

    return product

@core_router.get("/my-shops", response=List[ShopOut])
def list_my_shops_endpoint(request, user_id: int):

    return Shop.objects.filter(owner__owner__user_id=user_id).select_related('owner__owner')

@core_router.get('/shops/{shop_id}/products', response=List[ProductOut])
def product_list_endpoint(request, shop_id: uuid.UUID):
    # ninja легче работать напрямую через QuerySet, чем через переменные. Переменные могут вызывать ошибки
    return Product.objects.filter(shop=shop_id, is_active=True).select_related('shop') 


@core_router.patch("/product/{product_id}", response=ProductOut)
def edit_products_endpoint(request, product_id: int , data: ProductPatch):

    product = get_object_or_404(
            Product, 
            id=product_id, 
            shop__owner__owner__user_id=data.user_id
        )

    update_data = data.dict(exclude_unset=True)

    update_data.pop("user_id", None)

    for field, value in update_data.items():
        if field == "price" and value < 0:
            raise NegativePriceError("Цена не может быть отрицательной!")
        setattr(product, field, value)
    

    product.save()

    return product

@core_router.get("/products", response=List[ProductOut])
@paginate
def list_products_endpoint(request):
    return Product.objects.all()

@core_router.delete("/product/{product_id}", response={204: None})
def delete_product_endpoint(request, product_id: int, owner_id: int):
    
    product = get_object_or_404(
        Product,
        id=product_id,
        shop__owner__owner__user_id=owner_id
    )

    product.delete()

    return 204, None

