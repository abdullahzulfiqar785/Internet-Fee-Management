import random
from .models import Customer, Fee
import datetime
from dateutil import relativedelta


def get_id():
    number = random.randint(1000, 9999)
    while Customer.objects.filter(customer_id=number).exists():
        number = random.randint(1000, 9999)
    return number


def get_date(obj,):
    if not Fee.objects.filter(customer=obj.customer).exists():
        return datetime.date.today()
    reciept_date = Fee.objects.filter(
        customer=obj.customer).latest('pay_date').pay_date
    if datetime.date.today().day <= 28:
        reciept_date = reciept_date.replace(
            day=datetime.date.today().day)
    current_reciept_date = reciept_date + \
        relativedelta.relativedelta(months=1)
    return current_reciept_date
