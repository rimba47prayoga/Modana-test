from django.db import models


class Payment(models.Model):
    IDR = 'IDR'
    USD = 'USD'
    CURRENCY_CHOICES = (
        (USD, 'USD'),
        (IDR, 'IDR')
    )

    amount = models.DecimalField(decimal_places=2, max_digits=10)
    currency = models.CharField(max_length=10, choices=CURRENCY_CHOICES)
