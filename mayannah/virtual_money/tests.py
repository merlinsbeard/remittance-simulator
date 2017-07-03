from django.test import TestCase
from .models import Transaction
from django.contrib.auth.models import User


def create_user(username):
    person = User.objects.create(username=username)
    return person


def create_transaction(reference_id,
                       receiver,
                       sender,
                       amount,
                       is_deposit):
    transaction = Transaction.objects.create(
                        reference_id=reference_id,
                        sender=sender,
                        receiver=receiver,
                        amount=amount,
                        is_deposit=is_deposit)
    return transaction


class TransactionTestCase(TestCase):

    def test_transaction_deposits_exists(self):
        person1 = create_user("person_1")
        person2 = create_user("person_2")
        person3 = create_user("person_3")

        transaction1 = create_transaction("transaction_1",
                                          person1,
                                          person2,
                                          500,
                                          True)

        transaction2 = create_transaction("transaction_2",
                                          person1,
                                          person2,
                                          500,
                                          True)
        transaction3 = create_transaction("transaction_3",
                                          person1,
                                          person1,
                                          500,
                                          False)
        deposits = Transaction.deposits.all()
        self.assertEqual(deposits.count(), 2)

    def test_total_deposits(self):
        """Test for total number of deposits minus withdrawal."""
        person1 = create_user("person_1")
        person2 = create_user("person_2")
        transaction1 = create_transaction(
                        reference_id="transaction_4",
                        sender=person1,
                        receiver=person2,
                        amount=500,
                        is_deposit=True)

        transaction2 = create_transaction(
                        reference_id="transaction_5",
                        sender=person1,
                        receiver=person2,
                        amount=500,
                        is_deposit=True)

        transaction3 = create_transaction(
                        reference_id="transaction_6",
                        sender=person1,
                        receiver=person2,
                        amount=250,
                        is_deposit=False)
        deposits = Transaction.deposits.receive(person2)
        deposits = sum([t.amount for t in deposits])
        withdrawals = Transaction.withdraws.receive(person2)
        withdrawals = sum([t.amount for t in withdrawals])
        money = deposits - withdrawals
        # Sum of all deposits
        self.assertEqual(deposits, 1000)
        # sum of all withdrawals
        self.assertEqual(withdrawals, 250)
        # Total virtual money
        self.asserEqual(money, 750)
