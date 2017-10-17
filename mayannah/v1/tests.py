from django.test import TestCase
from virtual_money.models import TransactionHistory, Branch
from django.contrib.auth.models import User
from rest_framework.test import force_authenticate, APIRequestFactory
from .views import TransactionCreate, TransactionPay


class TransactionAPITestCase(TestCase):
    def setUp(self):
        # Users
        person1 = User.objects.create(username="person1")
        person2 = User.objects.create(username="person2")
        # Branches
        branch1 = Branch.objects.create(name="branch1", slug="branch1")
        # Transactions
        TransactionHistory.objects.create(reference_id="t1",
                                          account=person1,
                                          branch=branch1,
                                          amount=500,
                                          type="WITHDRAW")
        TransactionHistory.objects.create(reference_id="t2",
                                          account=person2,
                                          branch=branch1,
                                          amount=500,
                                          type="DEPOSIT")
        TransactionHistory.objects.create(reference_id="t3",
                                          account=person1,
                                          branch=branch1,
                                          amount=500,
                                          type="DEPOSIT")
        TransactionHistory.objects.create(reference_id="t4",
                                          account=person1,
                                          branch=branch1,
                                          amount=500,
                                          type="DEPOSIT",
                                          status="PAID")

    def test_complete(self):
        person1 = User.objects.get(username="person1")
        ths = TransactionHistory.objects.filter(account=person1)
        ths.filter(status="PAID")
        self.assertEqual(ths.count(), 3)

    def test_deposit(self):
        payload = {
                   "account": "person1",
                   "branch":  "branch1",
                   "amount": "200",
                   "type": "DEPOSIT"
                  }
        url = "/v1/transaction/"
        person1 = User.objects.get(username="person1")
        factory = APIRequestFactory()
        request = factory.post(
                               url,
                               payload,
                               )
        force_authenticate(request, user=person1)
        view = TransactionCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        data = response.data
        reference_id = data['reference_id']
        self.assertEqual(data['account'], "person1")
        self.assertEqual(data['branch'], "branch1")
        self.assertEqual(data['amount'], 200)
        self.assertEqual(data['type'], "DEPOSIT")
        transaction = TransactionHistory.objects.get(
                                reference_id=reference_id)
        self.assertEqual(transaction.status, "AVAILABLE")
        # Pay or complete the transaction
        pay_payload = {"reference_id": transaction.reference_id}
        pay_url = url + "complete/"
        request = factory.post(pay_url, pay_payload)
        force_authenticate(request, user=person1)
        view = TransactionPay.as_view()
        response = view(request)
        data = response.data
        self.assertEqual(data['message'], 'Successfully Tagged as Paid')

    def test_withdraw(self):
        payload = {
                   "account": "person1",
                   "branch":  "branch1",
                   "amount": "200",
                   "type": "WITHDRAW"
                  }
        url = "/v1/transaction/"
        person1 = User.objects.get(username="person1")
        factory = APIRequestFactory()
        request = factory.post(
                               url,
                               payload,
                               )
        force_authenticate(request, user=person1)
        view = TransactionCreate.as_view()
        response = view(request)
        self.assertEqual(response.status_code, 201)
        data = response.data
        reference_id = data['reference_id']
        self.assertEqual(data['account'], "person1")
        self.assertEqual(data['branch'], "branch1")
        self.assertEqual(data['amount'], 200)
        self.assertEqual(data['type'], "WITHDRAW")
        transaction = TransactionHistory.objects.get(
                                reference_id=reference_id)
        self.assertEqual(transaction.status, "AVAILABLE")
        # Pay or complete the transaction
        pay_payload = {"reference_id": transaction.reference_id}
        pay_url = url + "complete/"
        request = factory.post(pay_url, pay_payload)
        force_authenticate(request, user=person1)
        view = TransactionPay.as_view()
        response = view(request)
        data = response.data
        self.assertEqual(data['message'], 'Successfully Tagged as Paid')

    def test_deposit_fail(self):
        payload = {
                   "account": "person3",
                   "branch":  "branch1",
                   "amount": "200",
                   "type": "DEPOSIT"
                  }
        url = "/v1/transaction/"
        person1 = User.objects.get(username="person1")
        factory = APIRequestFactory()
        request = factory.post(
                               url,
                               payload,
                               )
        force_authenticate(request, user=person1)
        view = TransactionCreate.as_view()
        response = view(request)
        data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['account'][0], "User Not Existing")

    def test_withdraw_fail(self):
        """Withdraw with low money"""
        payload = {
                   "account": "person1",
                   "branch":  "branch1",
                   "amount": "2000",
                   "type": "WITHDRAW"
                  }
        url = "/v1/transaction/"
        person1 = User.objects.get(username="person1")
        factory = APIRequestFactory()
        request = factory.post(
                               url,
                               payload,
                               )
        force_authenticate(request, user=person1)
        view = TransactionCreate.as_view()
        response = view(request)
        data = response.data
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['non_field_errors'][0],
                         "Not enough money to withdraw")
