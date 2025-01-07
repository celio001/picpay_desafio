from ninja import NinjaAPI
from users.api import users_router

api = NinjaAPI()

api.add_router('users/', users_router)