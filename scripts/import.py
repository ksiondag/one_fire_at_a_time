import argparse
import csv

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


def main(args):
    parser = argparse.ArgumentParser(description="Import Betterment transaction CSV into fires")
    parser.add_argument("filename")
    args = parser.parse_args(args)

    parse_betterment_transactions(args.filename)


if __name__ == "__main__":
    import sys
    main(sys.argv[1:])
