from django.db import transaction, IntegrityError
from django.db import models
from django.db.models import F
from django.utils.translation import gettext_lazy as _
from .models import (
    TelegramUser,
    Tariff,
    Order, 
    OrderItem,
    OrderHistory, 
    Product, 
    CartItem, 
    CustomerProfile,
    OwnerProfile, 
    Shop,
    ProductImage
)


class OrderStatus(models.TextChoices):
    PENDING = "pending", _("Ожидает оплаты")
    PAID = "paid", _("Оплачен")
    SHIPPED = "shipped", _("Отправлен")
    COMPLETED = "completed", _("Завершен")
    CANCELED = "canceled", _("Отменен")


class ProfileRole(models.TextChoices):
    CUSTOMER = "customer", _("Покупатель")
    OWNER = "owner", _("Владелец")


def create_order(customer: CustomerProfile, shop: Shop, cart_item: CartItem) -> Order:
        
    try:
        with transaction.atomic(): # Атомарные операции проходят либо полностью, либо отменяются полностью из за любой ошибки
            # 1) Проверить корзину
            if not cart_item.exists():
                    return
            # 2) Создать заказ
            order = Order.objects.create(customer=customer, shop=shop)
            total_price = 0

            for item in cart_item:

                Product.objects.filter(id=item.product.id).update(stock=F("stock") - item.quantity) # Изменить остаток

                OrderItem.objects.create( # Создать товары заказа
                    order=order,
                    product=item.product,
                    product_name=item.product.title,
                    quantity=item.quantity,
                    price_per_item=item.product.price
                )

                total_price += item.product.price * item.quantity # Посчитать общую цену

            order.total_price = total_price # Записать общую цену
            order.save() # Сохраняем изменения

            cart_item.delete() # Удалить корзину

            return order # "Отчитываемся" о том, что мы создали для frontend

    except IntegrityError:
        return f"Ошибка! Товара недостаточно"

def set_main_image(image_id: int) -> None: # Айди фотки из api

    with transaction.atomic():
        image_obj = ProductImage.objects.get(id=image_id)
        ProductImage.objects.filter(product=image_obj.product).update(is_main=False)
        image_obj.is_main = True
        image_obj.save(update_fields=['is_main'])

def delete_image(image_id: int) -> None: # Айди фотки из api

    with transaction.atomic():
        image_obj = ProductImage.objects.get(id=image_id)
        was_main = image_obj.is_main
        product = image_obj.product
        image_obj.image.delete(save=False)
        image_obj.delete()

        if was_main:
            first_image = ProductImage.objects.filter(product=product).first()
            if first_image:
                set_main_image(first_image.id)

def change_order_status(order: Order, new_status: str) -> Order:

    with transaction.atomic():

        if new_status not in OrderStatus.values:
            raise ValueError("Недопустимый статус")
        
        if order.status == new_status:
            return order
        
        OrderHistory.objects.create( # Create не требует после себя метода save
            order=order,
            old_status=order.status,
            new_status=new_status
        )

        order.status = new_status # А вот здесь метод save будет нужен
        order.save(update_fields=['status']) # Говорим что именно сохранить в базе данных. + к оптимизации

        return order
    
def create_user(telegram_id: int, 
                role: str, 
                inn: str = None, 
                brand_name: str = None, 
                phone_number: str = None,
                tariff: Tariff = None) -> TelegramUser:
      
      with transaction.atomic():

        if role not in ProfileRole.values:
            raise ValueError("Такой роли не существует!")
        
        if TelegramUser.objects.filter(user_id=telegram_id).exists():
            raise ValueError("Такой пользователь уже существует!")
        
        tg_user = TelegramUser.objects.create(
            user_id=telegram_id,
            role=role
        )

        if role == ProfileRole.OWNER.value:
            create_owner_profile(user=tg_user, inn=inn, brand_name=brand_name, tariff=tariff, phone_number=phone_number)
        else:
            create_customer_profile(user=tg_user, phone_number=phone_number)

        return tg_user

def create_customer_profile(user: TelegramUser, phone_number: str) -> CustomerProfile:

    with transaction.atomic():
        return CustomerProfile.objects.create(
            customer=user,
            phone=phone_number
        )
        
def create_owner_profile(user: TelegramUser, inn: str, brand_name: str, tariff: Tariff = None, phone_number: str = None) -> OwnerProfile:
    with transaction.atomic():

        owner_tariff = tariff

        if not tariff:
            owner_tariff = Tariff.objects.get_or_create(plan="Бесплатный")[0] # Этот метод создает кортеж, поэтому достаем первую запись
 
        return OwnerProfile.objects.create(
            owner=user,
            tariff=owner_tariff,
            brand_name=brand_name,
            owner_inn=inn,
            phone=phone_number
        )