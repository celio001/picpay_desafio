from ninja import ModelSchema, Schema
from .models import Transactions
from decimal import Decimal

class TransactionSchema(Schema):
    amount: Decimal
    payer_id: int
    wallet_id: str