from django.db import transaction, IntegrityError
from django.db.models import F
from .models import OrderItem, Product, Order, ProductImage

def create_order(customer, shop , cart_item):

        try:
            with transaction.atomic():
                # 1) Проверить корзину
                if not cart_item.exists():
                     return
                # 2) Создать заказ
                order = Order.objects.create(customer=customer, shop=shop)
                total_price = 0

                for item in cart_item:

                    Product.objects.filter(id=item.product.id).update(stock=F("stock") - item.quantity) # Изменить остаток

                    OrderItem.objects.create( # Создать заказ
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

def set_main_image(image_id): # Айди фотки из api

    with transaction.atomic():
        image_obj = ProductImage.objects.get(id=image_id)
        ProductImage.objects.filter(product=image_obj.product).update(is_main=False)
        image_obj.is_main = True
        image_obj.save(update_fields=['is_main'])

def delete_image(image_id): # Айди фотки из api

    with transaction.atomic():
        image_obj = ProductImage.objects.get(id=image_id)
        was_main = image_obj.is_main

        if was_main:
            image_obj.image.delete(save=False)
            image_obj.delete()
            first_image = ProductImage.objects.filter(product=image_obj.product).first()
            set_main_image(first_image.id)
        else:
            image_obj.image.delete(save=False)
            image_obj.delete()
            



        
        
