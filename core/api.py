from ninja import Router
from .models import TelegramUser
from .schemas import TelegramUserOut

core_router = Router()

# Эндпоинты (Endpoints) — это, по сути, «адреса», 
# по которым твой фронтенд (или Telegram-бот) будет обращаться к твоему бэкенду за данными.

@core_router.get("/hello/{user_id}", response=TelegramUserOut) # Что то похожее на эндпоинт
def get_user(request, user_id: int): # Что будет принимать функция
    user = TelegramUser.objects.get(user_id=user_id)
    return user

# TODO: сделать api для одной из моделей(начнем с product)