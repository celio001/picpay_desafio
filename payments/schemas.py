from ninja import ModelSchema, Schema
from .models import Transactions

class TransactionSchema(ModelSchema):
    class Meta:
        model = Transactions
        exclude = ['id', 'date']