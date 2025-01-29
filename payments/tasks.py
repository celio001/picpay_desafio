from celery import shared_task
from django.db import transaction as django_transaction
from .models import Transactions
from users.models import User
import requests
from django.conf import settings

@shared_task
def enviar_email():
    return print('E-mail enviado com sucesso')

@shared_task
def transfer(payer_id,payee_id,transaction_amount, transaction_payer_id):
    with django_transaction.atomic():
        payer = User.objects.get(id=payer_id)
        payee = User.objects.get(id=payee_id)
        payer.pay(transaction_amount)
        payee.receive(transaction_amount)

        transct = Transactions(
            amount=transaction_amount,
            payer_id=transaction_payer_id,
            payee=payee
        )
        payer.save()
        payee.save()
        transct.save()

        #response1 = requests.get(settings.AUTHORIZE_TRANSFER_ENDPOINT)
        response = requests.get(settings.AUTHORIZE_TRANSFER_ENDPOINT).json()
        #print("Resposta do endpoint:", response1.text)  # Mostra o conteúdo exato da resposta
        
        if response.get('status') != 'authorized':
            raise Exception()