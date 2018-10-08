import random
import string
from django.db import models


def random_string():
    letters = string.hexdigits
    return ''.join(random.choice(letters) for _ in range(6))


class Document(models.Model):
    summary = models.CharField(max_length=254)
    text = models.TextField()

    date = models.DateField()
    added_time = models.DateTimeField()

    number = models.IntegerField()


class CharPrimaryKeyDocument(models.Model):
    id = models.CharField(primary_key=True, max_length=6, editable=False, default=random_string)
    text = models.TextField()
