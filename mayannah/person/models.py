from django.db import models
from django.contrib.auth.models import User
from coolname import generate_slug


class Person(models.Model):
    """
    Person is the User object with description and slug.

    Different from partner.models.Person.
    """
    user = models.OneToOneField(User)
    description_short = models.CharField(
                    max_length=255, blank=True)
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True, blank=True)

    def __str__(self):
        return self.user.username

    def save(self, *args, **kwargs):
        self.slug = generate_slug()
        super(Person, self).save(*args, **kwargs)
