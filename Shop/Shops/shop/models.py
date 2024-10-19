from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=100)
    latitude = models.FloatField(
        validators=[MinValueValidator(-90.0), MaxValueValidator(90.0)]
    )
    longitude = models.FloatField(
        validators=[MinValueValidator(-180.0), MaxValueValidator(180.0)]
    )

    def __str__(self):
        return self.name
