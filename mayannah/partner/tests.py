from django.test import TestCase
from .models import Person, Remittance


def create_person(first_name, last_name,
                  address, identification_id,
                  identification_type):
    person = Person.objects.create(first_name=first_name,
                                   last_name=last_name,
                                   address=address,
                                   identification_id=identification_id,
                                   identification_type=identification_type)
    return person


def create_remittance(source_reference_number,
                      remitter,
                      beneficiary,
                      payout_amount):
    remittance = Remittance.objects.create(
            source_reference_number=source_reference_number,
            remitter=remitter,
            beneficiary=beneficiary,
            payout_amount=payout_amount)
    return remittance


class RemittanceTests(TestCase):

    # Models
    def test_slug_save(self):
        remitter = create_person("Remi", "ter", "Manila", "321321321", "SSS")
        beneficiary = remitter
        remittance = create_remittance("uno-remit",
                                       remitter, beneficiary, 1000)
        self.assertEqual(remittance.slug, "uno-remit")

    def test_remittance_page(self):
        response = self.client.get('/remittance/')
        self.assertEqual(response.status_code, 200)
