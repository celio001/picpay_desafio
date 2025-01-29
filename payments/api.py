from ninja import Router
from .schemas import TransactionSchema
from django.shortcuts import get_object_or_404
from users.models import User
from rolepermissions. checkers import has_permission
from django.db import transaction as django_transaction
import requests
from django.conf import settings
from .models import Transactions
from .tasks import enviar_email, transfer
from core.auth import JWTAuth


payments_router = Router()

@payments_router.post('/', response={200: dict, 400: dict, 403: dict}, auth=JWTAuth())
def transaction(request, transaction: TransactionSchema):
    payer = get_object_or_404(User, id=transaction.payer_id)
    payee = get_object_or_404(User, wallet_id=transaction.wallet_id)

    if payer.amount < transaction.amount:
        return 400, {'error': 'Saldo insuficiente'}
    
    if not has_permission(payer, 'make_transfer'):
        return 403, {'error': 'Você não possui permissão para realizar transferência'}
    
    if not has_permission(payee, 'receive_transfer'):
        return 403, {'error': 'O usuario não possui permissão para receber transferência'}
    
    transfer.delay(payer.id,payee.id,transaction.amount, transaction.payer_id)

    # Retornar dados simulados da transação
    enviar_email.delay()
    return 200, {
        "amount": transaction.amount,
        "payer_id": payer.id,
        "payee_id": payee.id,
    }