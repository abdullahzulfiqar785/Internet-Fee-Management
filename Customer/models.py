from django.db import models
from django.contrib.auth.models import User
from Lookup.models import Area, Amount
# Create your models here.


class Customer(models.Model):
    customer_id = models.CharField(unique=True, max_length=4)
    phone = models.CharField(max_length=13)
    name = models.CharField(max_length=255)
    address = models.TextField()
    area = models.ForeignKey(
        Area, on_delete=models.PROTECT, related_name='customers')
    fee = models.ForeignKey(
        Amount, on_delete=models.PROTECT, related_name='customer_fee')

    def __str__(self) -> str:
        return str(self.customer_id)+"--"+str(self.name) + "--"+str(self.area.name)


class Fee(models.Model):
    customer = models.ForeignKey(
        Customer, on_delete=models.PROTECT, related_name='fee_items')
    recipient = models.ForeignKey(
        User, on_delete=models.SET_NULL, related_name='recipient_vouchers', null=True)
    amount_paid = models.PositiveSmallIntegerField()
    pay_date = models.DateField()
    credit = models.IntegerField(default=0)

    def __str__(self) -> str:
        return str(self.customer.name)

    class Meta:
        ordering = ['-pay_date']
