from partner.models import Remittance
from .serializers import RemittanceSerializer, RemittancePaySerializer
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated

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


class RemittanceDetail(generics.RetrieveUpdateAPIView):
    """Returns the specific remittance detail based on slug.

    Has GET and PUT

    GET is used to retrieve the details of Remittance
    Usage:
        GET /v1/remittance/<slug>

    PUT is used to update a specific field of remittance
    Usage:
        PUT /v1/remittance/<slug>
    """
    queryset = Remittance.objects.all()
    serializer_class = RemittanceSerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)


class RemittancePay(generics.GenericAPIView):
    """Tag Remittance Transaction as Paid."""
    queryset = Remittance.objects.all()
    serializer_class = RemittancePaySerializer
    authentication_classes = (BasicAuthentication,)
    permission_classes = (IsAuthenticated,)
    lookup_field = 'slug'

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
        remittance = self.get_object()
        data = request.data

        status_check = self.status_check(remittance.status)
        if status_check['status'] != "Success":
            return Response(status_check, status=status_check['code'])

        if data['source_reference_number'] == remittance.source_reference_number:
            """Pay Remittance"""
            remittance.status = "PAID"
            remittance.save()
            message = "Successfully Tagged as Paid"
            return Response({"message": message})
        else:
            return Response({"FAIL": "FAIL"})
