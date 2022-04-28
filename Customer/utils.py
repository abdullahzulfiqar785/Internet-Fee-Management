import random
from .models import Customer


def get_id():
    number = random.randint(1000, 9999)
    while Customer.objects.filter(customer_id=number).exists():
        number = random.randint(1000, 9999)
    return number
