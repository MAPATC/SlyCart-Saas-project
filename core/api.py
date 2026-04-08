from ninja import Router
from .models import TelegramUser
from .services import create_user
from .schemas import TelegramUserOut, TelegramUserIn

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
    

# TODO: сделать api для одной из моделей(начнем с product)