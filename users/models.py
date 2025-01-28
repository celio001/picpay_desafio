from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal
from .validators import validate_cpf
from secrets import token_hex

class User(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True, validators=[validate_cpf])
    email = models.EmailField(unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2, default=Decimal('0.00'))
    wallet_id = models.CharField(max_length=20, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        self.cpf = self.cpf.replace('.', '').replace('-', '')
        if not self.wallet_id:
            self.wallet_id = self.generate_wallet_id()
            
        super(User, self).save(*args, **kwargs)

    def pay(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise TypeError('Value deve ser um Decimal')
        
        self.amount -= value
    
    def receive(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise TypeError('Value deve ser um Decimal')
        
        self.amount += value
    
    def generate_wallet_id(self):
        while True:
            new_wallet_id = token_hex(10)
            exists = User.objects.filter(wallet_id=new_wallet_id)
            if not exists:
                return new_wallet_id