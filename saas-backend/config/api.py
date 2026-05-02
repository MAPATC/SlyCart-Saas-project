from ninja import NinjaAPI
from core.api import core_router

api = NinjaAPI()

api.add_router("/core/", core_router)

