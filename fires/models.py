from datetime import date
import math

from django.db import models

# TODO: These could be something set by the user on a per account basis
THRESHOLD_INTEREST_RATE = 0.03
SAFE_WITHDRAWAL_RATE = 0.04


def _today():
    return date.today()


def _days_between(previous_date, current_date):
    return (current_date - previous_date).days


def _annual_to_n_days(rate, days):
    return math.pow(rate, days/365.)


class FireManager(models.Manager):
    def create_with_fund_allocation(self, name, fund, allocation, percentage=True):
        if not percentage:
            allocation = 100*1000 * allocation / fund.balance

        unallocated = 100*1000 - sum(FireDistribution.objects.filter(fund=fund).values_list("allocation", flat=True))
        if allocation > unallocated:
            raise ValueError("{} does not have enough unallocated funds to fuel this FIRE".format(fund.name))

        fire = self.create(name=name, threshold_balance=int(fund.balance * allocation/100000.), threshold_date=fund.balance_date, previous_withdrawal=date.today())
        FireDistribution.objects.create(fund=fund, fire=fire, allocation=allocation)
        return fire

    def create_empty_fund(self, name):
        return self.create(name=name, threshold_balance=0, threshold_date=date.today(), previous_withdrawal=date.today())


class Fire(models.Model):
    objects = FireManager()

    name = models.CharField(unique=True, max_length=255)
    threshold_balance = models.IntegerField(null=False)
    threshold_date = models.DateField(null=False)

    previous_withdrawal = models.DateField(null=False)

    funds = models.ManyToManyField("Fund", through="FireDistribution")

    def threshold_balance_for_today(self):
        today = _today()
        days = _days_between(self.threshold_date, today)
        rate = 1 + THRESHOLD_INTEREST_RATE
        return int(self.threshold_balance * _annual_to_n_days(rate, days))

    def safe_withdrawal_amount(self):
        today = _today()
        days = _days_between(self.previous_withdrawal, today)
        return int(self.balance * _annual_to_n_days(SAFE_WITHDRAWAL_RATE, days))

    def update_allocation(self, delta, percentage=True, fund=None):
        """
        Update allocation of fire by delta in given fund or across all funds
        that the fire is fueled by.

        Args:
            delta - Amount changed
            percentage - Is the delta is in percentage of balance or not?
            fund - Specific fund to update allocation of
        """


    @property
    def balance(self):
        total_balance = 0
        for balance, allocation in FireDistribution.objects.filter(fire=self).values_list("fund__balance", "allocation"):
            allocation = allocation / 100000.
            total_balance += balance * allocation

        return int(total_balance)

    @property
    def balance_date(self):
        ret = None
        for d in self.funds.all().values_list("balance_date", flat=True):
            if ret is None or d > ret:
                ret = d

        return ret if ret else date.today()


class Fund(models.Model):
    name = models.CharField(unique=True, max_length=255)
    balance = models.IntegerField(default=0)
    balance_date = models.DateField(null=False)


# TODO: make an option for balance history with a record of balance changes and what type they were


class FireDistribution(models.Model):
    class Meta:
        unique_together = ["fund", "fire"]

    fund = models.ForeignKey("Fund", null=False, on_delete=models.CASCADE)
    fire = models.ForeignKey("Fire", null=False, on_delete=models.CASCADE)
    allocation = models.IntegerField(default=0)
