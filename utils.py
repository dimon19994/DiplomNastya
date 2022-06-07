import random
from peewee import fn
from random import shuffle

from constants import LotStatuses, DEFAULT_PRIORITY, AccountType
from models import Electricity, Lot, User


def get_request_data(request):
    return dict(request.json or request.form.items() or {})


def get_base_58_string(length=12):
    symbols = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
    return ''.join([random.choice(symbols) for _ in range(length)])


def convert_from_wei(amount_in_wei, precision=8):
    return round(amount_in_wei / 10 ** 18, precision)


def convert_to_wei(amount_in_eth):
    return int(float('{0:.8f}e+18'.format(amount_in_eth)))


def sort_by_priority(electricities):
    result = []
    for i in DEFAULT_PRIORITY['buy']:
        for electricity in electricities:
            if electricity.user.account_type == i:
                result.append(electricity)

    return result


def additional_order_kilowatts(total_kilowatts, aggregator):
    electricities = Electricity.select(Electricity).join(User) \
        .having((User.account_type == AccountType.Salesman) &
                (fn.sum(Electricity.total_kilowatts - Electricity.total_kilowatts_freeze) > 0)) \
        .group_by(Electricity, User.account_type)

    if len(electricities) == 0:
        electricities = Electricity.select(Electricity).join(User) \
            .having((fn.sum(Electricity.total_kilowatts - Electricity.total_kilowatts_freeze) > 0)) \
            .group_by(Electricity, User.account_type) \
            .order_by(Electricity.id)

    total_free_kilowatts = sum(
        [(electricity.total_kilowatts - electricity.total_kilowatts_freeze) for electricity in electricities])

    preorder = {"kilowatt_count": 0, "amount": 0}

    if total_free_kilowatts > total_kilowatts:
        for electricity in electricities:
            if electricity.user != aggregator:
                free_kilowatts_count = electricity.total_kilowatts - electricity.total_kilowatts_freeze
                if free_kilowatts_count > total_kilowatts:
                    free_kilowatts_count = total_kilowatts

                total_kilowatts -= free_kilowatts_count

                preorder["kilowatt_count"] += free_kilowatts_count
                preorder["amount"] += free_kilowatts_count * electricity.amount_per_kilowatt
                electricity.total_kilowatts_freeze += free_kilowatts_count
                electricity.save()

        average_price = preorder["amount"] / preorder["kilowatt_count"]

        Lot.create(status=LotStatuses.New, aggregator=aggregator, average_price=average_price,
                   kilowatts_number=preorder["kilowatt_count"])
        aggregator.wallet.balance -= preorder["amount"]
        aggregator.wallet.save()
