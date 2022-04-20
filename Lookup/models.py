from django.db import models

# Create your models here.


class Area(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Amount(models.Model):
    amount = models.IntegerField(unique=True)

    def __str__(self) -> str:
        return str(self.amount)
