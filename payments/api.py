from ninja import Router
from .schemas import TransactionSchema
from django.shortcuts import get_object_or_404
from users.models import User
from rolepermissions. checkers import has_permission

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
    # Retornar dados simulados da transação
    return 200, {
        "amount": transaction.amount,
        "payer": payer.id,
        "payee": payee.id,
    }