from django.db import models
from django.contrib.auth.models import User
import uuid


STATUS = (
        ("AVAILABLE", "AVAILABLE"),
        ("COMPLETE", "COMPLETE"),
        ("PAID", "PAID"),
        ("CANCELLED", "CANCELLED"),
)

TRANSACTION_TYPE = (
        ("DEPOSIT", "DEPOSIT"),
        ("WITHDRAW", "WITHDRAW"),
        ("TRANSFER", "TRANSFER"),
)


class Transaction(models.Model):
    """Model for Transaction.

    reference_id is the unique identifier for the model

    Transaction types:

        1. Deposit
        Cash turned into virtual currency

        2. Withdraw
        Virtual Currency Turned into Cash

        3. Transfer
        Virtual Currency transfered to other accounts

    """
    reference_id = models.CharField(max_length=255, unique=True)
    remitter = models.ForeignKey(User, related_name='remitter')
    account = models.ForeignKey(User, related_name='account')
    amount = models.IntegerField()
    status = models.CharField(max_length=100,
                              choices=STATUS,
                              default="AVAILABLE")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=100,
                            choices=TRANSACTION_TYPE,
                            default="DEPOSIT")

    def __str__(self):
        return self.reference_id


class Branch(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class TransactionHistory(models.Model):
    reference_id = models.CharField(max_length=255, unique=True, default=uuid.uuid4, editable=False)
    account = models.ForeignKey(User)
    amount = models.IntegerField()
    status = models.CharField(max_length=100,
                              choices=STATUS,
                              default="AVAILABLE")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    type = models.CharField(max_length=100,
                            choices=TRANSACTION_TYPE,
                            default="DEPOSIT")
    branch = models.ForeignKey(Branch, related_name='branch')

    def __str__(self):
        return self.reference_id
