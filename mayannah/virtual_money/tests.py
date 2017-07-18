from django.test import TestCase
from .models import TransactionHistory, Branch
from django.contrib.auth.models import User


def create_user(username):
    person = User.objects.create(username=username)
    return person

def create_branch(branch):
    branch = Branch.objects.create(name=branch, slug=branch)
    return branch


def create_transaction(
                       account,
                       branch,
                       amount,
                       type):
    transaction = TransactionHistory.objects.create(
                        account=account,
                        branch=branch,
                        amount=amount,
                        type=type)
    return transaction


class TransactionTestCase(TestCase):

    def test_transaction_deposits_exists(self):
        person1 = create_user("person_1")
        person2 = create_user("person_2")
        person3 = create_user("person_3")

        branch1 = create_branch("branch1")

        transaction1 = create_transaction(person1,
                                          branch1,
                                          500,
                                          "WITHDRAW")

        transaction2 = create_transaction(person2,
                                          branch1,
                                          500,
                                          "DEPOSIT")
        transaction3 = create_transaction(person1,
                                          branch1,
                                          500,
                                          "DEPOSIT")
        deposits = TransactionHistory.objects.filter(type="DEPOSIT")
        self.assertEqual(deposits.count(), 2)

    def test_total_deposits(self):
        """Test for total number of deposits minus withdrawal."""
        person1 = create_user("person_1")
        person2 = create_user("person_2")
        branch1 = create_branch("branch1")
        transaction1 = create_transaction(
                        person1,
                        branch1,
                        500,
                        "DEPOSIT")

        self.assertEqual(transaction1.amount, 500)
