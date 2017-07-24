from partner.models import Remittance
from .serializers import RemittanceSerializer, RemittancePaySerializer, \
                         TransactionDetailSerializer, TransactionSerializer, \
                         TransactionCompleteSerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from virtual_money.models import Transaction, TransactionHistory
from django.db.models import Q
from django.contrib.auth.models import User

import arrow
import logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)


class RemittanceList(generics.ListCreateAPIView):
    """View and Create Remittance Transaction.

    Uses GET and POST

    Get Returns all Remittance Transactions

    Usage:
        GET <url>/v1/remittance

    Post creates a new Remittance Transaction
    Usage:
        POST <url>/v1/remittance
    """

    queryset = Remittance.objects.all()
    serializer_class = RemittanceSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)


class RemittanceGetDetail(generics.RetrieveUpdateAPIView):
    queryset = Remittance.objects.all()
    serializer_class = RemittanceSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RemittanceDetail(generics.GenericAPIView):
    """Returns the specific remittance detail.

    Has POST only

    POST is used to retrieve the details of Remittance
    Usage:
        POST /v1/remittance/search

        {"source_reference_number": "sample-uno"}

    """
    queryset = Remittance.objects.all()
    serializer_class = RemittanceSerializer

    def post(self, request, *args, **kwargs):
        data = request.data
        ref_num = data['source_reference_number']
        try:
            remittance = Remittance.objects.get(
                            source_reference_number=ref_num)
        except:
            return Response("ERROR", status=status.HTTP_400_BAD_REQUEST)

        serialized_data = RemittanceSerializer(remittance)

        return Response(serialized_data.data)

class RemittancePay(generics.GenericAPIView):
    """Tag Remittance Transaction as Paid."""
    queryset = Remittance.objects.all()
    serializer_class = RemittancePaySerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def status_check(self, remittance_status):
        codes = {
                "AVAILABLE": {
                    "status": "Success",
                    "code": status.HTTP_200_OK},
                "PAID": {
                    "status": "Already Paid Out",
                    "code": status.HTTP_200_OK},
                "CANCELLED": {
                    "status": "Transaction Cancelled",
                    "code": status.HTTP_423_LOCKED},
                "ERROR": {
                    "status": "ERROR",
                    "code": status.HTTP_404_NOT_FOUND},
                }

        for k, v in codes.items():
            logger.warning(f'k{k}-v{v}')
            if k == remittance_status:
                return v
        else:
            return codes['ERROR']

    def post(self, request, *args, **kwargs):
        data = request.data
        remittance = Remittance.objects.get(
                source_reference_number=data['source_reference_number'])

        status_check = self.status_check(remittance.status)
        if status_check['status'] != "Success":
            return Response(status_check, status=status_check['code'])

        if data['source_reference_number'] == remittance.source_reference_number:
            """Pay Remittance"""
            remittance.status = "PAID"
            now = arrow.now().datetime
            remittance.date_paid_out = now
            remittance.save()
            message = "Successfully Tagged as Paid"
            return Response({"message": message})
        else:
            return Response({"FAIL": "FAIL"}, status=status.HTTP_400_BAD_REQUEST)


class TransactionDetail(generics.RetrieveAPIView):
    serializer_class = TransactionDetailSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'reference_id'

    def get_queryset(self):
        user = self.request.user
        return TransactionHistory.objects.filter(account=user)

class TransactionCreate(generics.CreateAPIView):
    serializer_class = TransactionSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        data = request.data
        return self.create(request, *args, **kwargs)

def status_check(status):
    codes = {
            "AVAILABLE": {
                "status": "Success",
                "code": status.HTTP_200_OK},
            "PAID": {
                "status": "Already Paid Out",
                "code": status.HTTP_200_OK},
            "CANCELLED": {
                "status": "Transaction Cancelled",
                "code": status.HTTP_423_LOCKED},
            "ERROR": {
                "status": "ERROR",
                "code": status.HTTP_404_NOT_FOUND},
            }

    for k, v in codes.items():
        logger.warning(f'k{k}-v{v}')
        if k == remittance_status:
            return v
    else:
        return codes['ERROR']

class TransactionPay(generics.UpdateAPIView):
    serializer_class = TransactionCompleteSerializer
    authentication_classes = (BasicAuthentication,)


    def post(self, request, *args, **kwargs):
        data = request.data
        transaction = data['reference_id']

        message = {"status": "Success",
                "message": "Blank"}

        try:
            transaction = TransactionHistory.objects.get(reference_id=transaction)
        except Transaction.DoesNotExist:
            message['status'] = 'Error'
            message['message'] = "Does Not exists"
            return Response(message, status.HTTP_404_NOT_FOUND)

        if transaction.status == "PAID":
            return Response(
                    {"status": "Already Paid"},
                    status.HTTP_200_OK)
        elif transaction.status != "AVAILABLE":
            return Response(
                    {"status": "Not available"},
                    status.HTTP_404_NOT_FOUND)
        else:
            """Pay Remittance"""
            transaction.status = "PAID"
            now = arrow.now().datetime
            transaction.save()
            message = "Successfully Tagged as Paid"
        return Response({"message": message})
