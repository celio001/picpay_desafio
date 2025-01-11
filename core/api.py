from ninja import NinjaAPI
from users.api import users_router
from payments.api import payments_router

api = NinjaAPI()

api.add_router('users/', users_router)
api.add_router('payments/', payments_router)