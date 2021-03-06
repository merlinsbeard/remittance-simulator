from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _

STATUS = (
        ("AVAILABLE", "AVAILABLE"),
        ("PAID", "PAID"),
        ("CANCELLED", "CANCELLED"),
)


class Person(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    contact_number = models.CharField(max_length=20, blank=True)
    address = models.TextField(blank=True)
    country = models.CharField(max_length=255, default="Philippines")
    identification_type = models.CharField(max_length=255, blank=True)
    identification_id = models.CharField(max_length=255, blank=True)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.full_name()


class Remittance(models.Model):
    source_reference_number = models.CharField(max_length=255, unique=True)
    remitter = models.ForeignKey(Person, related_name="remitter")
    beneficiary = models.ForeignKey(Person, related_name="beneficiary")
    date_created = models.DateTimeField(auto_now_add=True)
    date_paid_out = models.DateTimeField(null=True, blank=True)
    payout_amount = models.IntegerField()
    payout_currency = models.CharField(max_length=10, default="PH")
    slug = models.SlugField(max_length=255, blank=True)
    status = models.CharField(max_length=100,
                              choices=STATUS,
                              default="AVAILABLE")

    def __str__(self):
        return self.source_reference_number

    def get_absolute_url(self):
        return reverse('partner:detail', kwargs={'slug': self.slug})

    def clean(self):
        amount = self.payout_amount
        cents = abs(amount) % 100
        if amount < 1000:
            raise ValidationError(_('Amount should be greater than 1000'))

        if cents > 0:
            raise ValidationError(_('No Cents Allowed'))

    def save(self, *args, **kwargs):
        """Source Reference Number is used as Slug."""
        self.slug = slugify(self.source_reference_number)
        super(Remittance, self).save(*args, **kwargs)
