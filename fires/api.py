from contextlib import contextmanager
from datetime import date

from fires.models import Fund


class FireAPI():
    def __init__(self):
        pass

    def get(self):
        pass

    def patch(self):
        pass

    def post(self):
        pass


@contextmanager
def fire_api():
    yield FireAPI()


class FundAPI():
    def post(self, name, balance, balance_date=None):
        if balance_date is None:
            balance_date = date.today()
        Fund.objects.create(name=name, balance=balance, balance_date=balance_date)


@contextmanager
def fund_api():
    yield FireAPI()
