from ninja import Schema, ModelSchema
from .models import User

class UserSchema(ModelSchema):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'cpf', 'email', 'password']

class TypeSchema(Schema):
    type: str

class TypeUserSchema(Schema):
    user: UserSchema
    type_user: TypeSchema