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


class Fire(models.Model):
    threshold_balance = models.IntegerField(default=0)
    threshold_date = models.DateField(null=False)

    balance = models.IntegerField(default=0)
    balance_date = models.DateField(null=False)

    previous_withdrawal = models.DateField(null=False)

    def threshold_balance_for_today(self):
        today = _today()
        days = _days_between(self.last_threshold_date, today)
        rate = 1 + THRESHOLD_INTEREST_RATE
        return self.threshold_balance * _annual_to_n_days(rate, days)

    def safe_withdrawal_amount(self):
        today = _today()
        days = _days_between(self.previous_withdrawal, today)
        return self.balance * _annual_to_n_days(SAFE_WITHDRAWAL_RATE, days)
