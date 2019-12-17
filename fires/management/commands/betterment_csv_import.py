import argparse
import csv

from django.core.management.base import BaseCommand

from fires.models import Fund, Fire

INTEREST_TRANSACTIONS = [
    "Market Change",
    "Dividend Reinvestment",
    "Advisory Fee",
]

IGNORABLE_KEYWORDS = [
    "Allocation",
    "Tax Loss Harvesting",
    "Portfolio Update",
    "Rebalance",
]


def parse_betterment_transactions(filename):
    betterment_transactions = csv.DictReader(open(filename, "r"))

    for transaction in betterment_transactions:
        transaction_descrpiton = transaction["Transaction Description"]
        if transaction_descrpiton in INTEREST_TRANSACTIONS:
            # TODO: Interest transaction to fund, spread across fires
            pass
        elif "Deposit" in transaction_descrpiton:
            # TODO: Deposit into fund, also interaction for fires
            pass
        elif "Withdrawal" in transaction_descrpiton:
            # TODO: Withdrawal from fund, also interaction for fires
            pass
        elif "Transfer" in transaction_descrpiton:
            # TODO: Transfer to/from another fund (probably needs to be interactive)
            pass
        elif any([word in transaction_descrpiton for word in IGNORABLE_KEYWORDS]):
            pass
        else:
            print(transaction_descrpiton)


def list_funds_and_fires():
    print("Funds:")
    for fund in Fund.objects.all():
        print("  {}".format(fund.name))
    print()

    print("Fires:")
    for fire in Fire.objects.all():
        print("  {}".format(fire.name))


class Command(BaseCommand):
    help="Import transaction history from Betterment export csv"

    def add_arguments(self, parser):
        parser.add_argument("filename")

    def handle(self, filename, *args, **kwargs):
        if filename == "list":
            list_funds_and_fires()
            return

        parse_betterment_transactions(filename)
