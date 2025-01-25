from celery import shared_task

@shared_task
def enviar_email():
    return print('E-mail enviado com sucesso')