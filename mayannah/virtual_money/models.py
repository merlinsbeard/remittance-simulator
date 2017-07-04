from django.db import models
from django.contrib.auth.models import User


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
