from datetime import datetime
import json
import uuid

from ninja_extra import NinjaExtraAPI, api_controller, http_post
from core.api import core_router
from ninja.renderers import JSONRenderer
from core.exceptions import UserAlreadyExistsError, PhoneNumberAlreadyTakenError
from ninja.responses import NinjaJSONEncoder
from ninja_jwt.schema import TokenObtainPairOutputSchema
from core.schemas import MyTokenObtainPairSchema

class UnicodeJSONRenderer(JSONRenderer):
    def render(self, request, data, *, response_status):
        return json.dumps(
            data, 
            cls=NinjaJSONEncoder, # добавили поддержку дат и чисел, так как базовый json это не поддерживает
            ensure_ascii=False
        ).encode("utf-8")


api = NinjaExtraAPI(renderer=UnicodeJSONRenderer())

@api.exception_handler(UserAlreadyExistsError)
def user_already_exists_handler(request, exc):

    return api.create_response(
        request=request,
        data={
            "detail": str(exc),
            "timestamp": datetime.now(),      # Сработает благодаря NinjaJSONEncoder
            "error_id": uuid.uuid4(),         # Сработает благодаря NinjaJSONEncoder
            "method": request.method,
            "is_authenticated": request.user.is_authenticated, 
            "user_status": "Guest" if request.user.is_anonymous else "Member",
            "path": request.path
            },
        status=400
    )

@api.exception_handler(PhoneNumberAlreadyTakenError)
def user_already_exists_handler(request, exc):

    return api.create_response(
        request=request,
        data={
            "detail": str(exc),
            "timestamp": datetime.now(),      # Сработает благодаря NinjaJSONEncoder
            "error_id": uuid.uuid4(),         # Сработает благодаря NinjaJSONEncoder
            "method": request.method,
            "is_authenticated": request.user.is_authenticated, 
            "user_status": "Guest" if request.user.is_anonymous else "Member",
            "path": request.path
            },
        status=400
    )

@api_controller('/auth', tags=['Auth']) # Обязательно через декоратор!
class MyTokenController:

    @http_post("/pair", response=TokenObtainPairOutputSchema)
    def obtain_token(self, user_token: MyTokenObtainPairSchema):
        # Метод to_response_schema теперь содержит всю логику поиска и генерации
        return user_token.to_response_schema()

api.add_router("/core/", core_router)
api.register_controllers(MyTokenController)

