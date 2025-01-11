from ninja import ModelSchema
from .models import Transactions

class TransactionSchema(ModelSchema):
    class Meta:
        model = Transactions
        exclude = ['id', 'date']