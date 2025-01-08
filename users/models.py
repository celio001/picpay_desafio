from django.db import models
from django.contrib.auth.models import AbstractUser
from decimal import Decimal

class User(AbstractUser):
    cpf = models.CharField(max_length=14, unique=True)
    email = models.EmailField(unique=True)
    amount = models.DecimalField(max_digits=15, decimal_places=2)

    def save(self, *args, **kwargs):
        self.cpf = self.cpf.replace('.', '').replace('-', '')
        super(User, self).save(*args, **kwargs)

    def pay(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise TypeError('Value deve ser um Decimal')
        
        self.amount -= value
    
    def receive(self, value: Decimal):
        if not isinstance(value, Decimal):
            raise TypeError('Value deve ser um Decimal')
        
        self.amount += value