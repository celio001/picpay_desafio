from ninja.security import HttpBearer
import jwt
from django.conf import settings
from users.models import User

class InvalidToken(Exception):
    pass

class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            data = jwt.decode(token, settings.SECRET_KEY_JWT, algorithms='HS256')
        except jwt.exceptions.ExpiredSignatureError:
            raise InvalidToken('Token expirado')
        except:
            raise InvalidToken('Token inválido')
        
        user = User.objects.filter(username=data['user']).first()
        if user:
            return user.id
        
        raise InvalidToken('Token inválido')
