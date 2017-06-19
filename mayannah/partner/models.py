from django.db import models
from django.utils.text import slugify

STATUS = (
        ("AVAILABLE", "AVAILABLE"),
        ("PAID", "PAID"),
        ("CANCELLED", "CANCELLED"),
)


class Person(models.Model):
    name = models.CharField(max_length=255)
    address = models.TextField()
    country = models.CharField(max_length=255, default="Philippines")
    identification_type = models.CharField(max_length=255)
    identification_id = models.CharField(max_length=255)

    def __str__(self):
        return self.name


class Remittance(models.Model):
    source_reference_number = models.CharField(max_length=255)
    remitter = models.ForeignKey(Person, related_name="remitter")
    beneficiary = models.ForeignKey(Person, related_name="beneficiary")
    date_created = models.DateTimeField(auto_now_add=True)
    payout_amount = models.IntegerField()
    payout_currency = models.CharField(max_length=10, default="PH")
    slug = models.SlugField(max_length=255, blank=True)
    status = models.CharField(max_length=100,
                              choices=STATUS,
                              default="AVAILABLE")

    def __str__(self):
        return self.source_reference_number

    def save(self, *args, **kwargs):
        """Source Reference Number is used as Slug."""
        self.slug = slugify(self.source_reference_number)
        super(Remittance, self).save(*args, **kwargs)
