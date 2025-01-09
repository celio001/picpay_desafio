from ninja import Router
from .schema import UserSchema
from .models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError

users_router = Router()

@users_router.post('/', response={200: dict, 400: dict, 500: dict})
def create_user(request, user: UserSchema):
    user = User(**user.dict())
    user.password =  make_password(user.password)
    try:
        user.full_clean()
        user.save()
    except ValidationError as e:
        return 400, {'errors': e.message_dict}
    
    except Exception as e:
        return 500, {'errors': 'Erro interno do Servidor'}
    return {'ok': 'ok'}