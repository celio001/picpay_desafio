from ninja import Router
from .schema import TypeUserSchema, UserLoginSchema
from .models import User
from django.contrib.auth.hashers import make_password
from django.core.exceptions import ValidationError
from rolepermissions.roles import assign_role
from datetime import datetime, timedelta
from django.contrib import auth
from django.conf import settings
import jwt

users_router = Router()

@users_router.post('/', response={200: dict, 400: dict, 500: dict})
def create_user(request, type_user_schema: TypeUserSchema):

    print(type_user_schema.dict())
    user = User(**type_user_schema.user.dict())
    user.password =  make_password(type_user_schema.user.password)
    
    try:
        user.full_clean()
        user.save()
        assign_role(user, type_user_schema.type_user.type)
    except ValidationError as e:
        return 400, {'errors': e.message_dict}
    
    except Exception:
        return 500, {'errors': 'Erro interno do Servidor'}
    
    return {'user_id': user.id,
            'username': user.username
            }

@users_router.post('/login/', response={200: dict, 401: dict})
def login(request, user_schema: UserLoginSchema):
    user = auth.authenticate(request,
                             username=user_schema.username,
                             password=user_schema.password)
    
    if not user: 
        return 401, {'Error': 'Email ou senha invalidos'}
    
    expiration_time = datetime.now() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE)

    payload = {
        'user': user.username,
        'exp': int(expiration_time.timestamp())
    }

    token = jwt.encode(payload, settings.SECRET_KEY_JWT, algorithm="HS256")
    return {'token': token}