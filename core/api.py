from ninja import Router
from .models import Product

core_router = Router()


@core_router.get("hello/")
def hello(request):
    return {"message": "Hello from Core"}


# TODO: сделать api для одной из моделей(начнем с product)