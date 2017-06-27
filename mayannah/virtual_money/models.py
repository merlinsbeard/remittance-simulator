from django.db import models
from django.contrib.auth.models import User


class DepositManager(models.Manager):
    """Filter deposit transactions only."""
    def get_queryset(self):
        return super(DepositManager,
                self).get_queryset().filter(is_deposit=True)

class WithdrawManager(models.Manager):
    """Filter not deposit transactions only."""
    def get_queryset(self):
        return super(DepositManager,
                self).get_queryset().filter(is_deposit=False)


class Transaction(models.Model):
    reference_id = models.CharField(max_length=255, unique=True)
    user = models.ForeignKey(User)
    amount = models.IntegerField()
    is_deposit = models.BooleanField(default=True)

    # Model Managers
    objects = models.Manager()
    deposits = DepositManager()
    withdraws = WithdrawManager()

    def __str__(self):
        return self.reference_id

