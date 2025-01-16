from django.db import models
from users.models import User
from decimal import Decimal

# Create your models here.
class Transactions(models.Model):
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'), editable=False)
    payer = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False)
    payee = models.ForeignKey(User, on_delete=models.DO_NOTHING, editable=False, related_name="payee_user")
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f' from {self.payer.first_name} to {self.payee.first_name} = R$ {self.amount}'