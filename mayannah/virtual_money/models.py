from django.db import models
from django.contrib.auth.models import User


STATUS = (
        ("AVAILABLE", "AVAILABLE"),
        ("COMPLETE", "COMPLETE"),
        ("PAID", "PAID"),
        ("CANCELLED", "CANCELLED"),
)


class DepositManager(models.Manager):
    """Filter deposit transactions only."""
    def get_queryset(self):
        return super(DepositManager,
                     self).get_queryset().filter(is_deposit=True)

    def receive(self, receiver):
        """Filter deposit transaction of receiver."""
        return super(
                DepositManager,
                self).get_queryset().filter(
                        is_deposit=True,
                        receiver=receiver)

    def send(self, sender):
        """Filter senders deposit transactions."""
        return super(
                DepositManager,
                self).get_queryset().filter(
                        is_deposit=True,
                        sender=sender)


class WithdrawManager(models.Manager):
    """Filter Withdrawal transactions only."""
    def get_queryset(self):
        return super(WithdrawManager,
                     self).get_queryset().filter(is_deposit=False)

    def receive(self, receiver):
        """Filter withdrawal transactions of receiver."""
        return super(
                WithdrawManager,
                self).get_queryset().filter(
                        is_deposit=False,
                        receiver=receiver)


class Transaction(models.Model):
    """Model for Transaction.

    reference_id is the unique identifier for the model
    """
    reference_id = models.CharField(max_length=255, unique=True)
    receiver = models.ForeignKey(User, related_name='receiver')
    sender = models.ForeignKey(User, related_name='sender')
    amount = models.IntegerField()
    status = models.CharField(max_length=100,
                              choices=STATUS,
                              default="AVAILABLE")
    is_deposit = models.BooleanField(default=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    # Model Managers
    objects = models.Manager()
    deposits = DepositManager()
    withdraws = WithdrawManager()

    def __str__(self):
        return self.reference_id
