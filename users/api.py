from ninja import Router

users_router = Router()

@users_router.post('/', response={200: dict})
def create_user(request):
    return {'ok': 'ok'}