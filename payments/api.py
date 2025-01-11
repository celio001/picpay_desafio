from ninja import Router

payments_router = Router()

@payments_router.post('/')
def transaction(request, transaciton: TransactionSchema):
    return {1: 1}