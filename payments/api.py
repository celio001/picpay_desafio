from ninja import Router
from .schemas import TransactionSchema
from django.shortcuts import get_object_or_404
from users.models import User
from rolepermissions. checkers import has_permission
from django.db import transaction as django_transaction
import requests
from django.conf import settings
from .models import Transactions
from .tasks import enviar_email


payments_router = Router()

@payments_router.post('/', response={200: TransactionSchema, 400: dict, 403: dict})
def transaction(request, transaction: TransactionSchema):
    payer = get_object_or_404(User, id=transaction.payer)
    payee = get_object_or_404(User, id=transaction.payee)

    if payer.amount < transaction.amount:
        return 400, {'error': 'Saldo insuficiente'}
    
    if not has_permission(payer, 'make_transfer'):
        return 403, {'error': 'Você não possui permissão para realizar transferência'}
    
    if not has_permission(payee, 'receive_transfer'):
        return 403, {'error': 'O usuario não possui permissão para receber transferência'}
    
    with django_transaction.atomic():
        payer.pay(transaction.amount)
        payee.receive(transaction.amount)

        transct = Transactions(
            amount=transaction.amount,
            payer_id=transaction.payer,
            payee_id=transaction.payee
        )
        payer.save()
        payee.save()
        transct.save()

        #response1 = requests.get(settings.AUTHORIZE_TRANSFER_ENDPOINT)
        response = requests.get(settings.AUTHORIZE_TRANSFER_ENDPOINT).json()
        #print("Resposta do endpoint:", response1.text)  # Mostra o conteúdo exato da resposta
        
        if response.get('status') != 'authorized':
            raise Exception()

    # Retornar dados simulados da transação
    enviar_email.delay()
    return 200, {
        "amount": transaction.amount,
        "payer_id": payer.id,
        "payee_id": payee.id,
    }