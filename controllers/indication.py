from datetime import datetime

from controllers import _Controller
from models import Indication, User, Lot, Electricity


class IndicationController(_Controller):
    def _post(self, aggregator_id, user_id):
        user = User.get_by_id(user_id)

        if user.addons.get("aggregator_id", -1) != aggregator_id:
            return {"error": "another aggregator id"}

        last_update = Indication.select(Indication.created).where(Indication.user_id == user_id).order_by(Indication.created.desc()).first()

        if last_update is not None:
            last_update_timestamp = last_update.created.timestamp()
            timestamp_now = datetime.now().timestamp()

            if not last_update_timestamp + 10 <= timestamp_now:
                return {"error": "So quickly"}

        kilowatts_count = self.request_data.get("kilowatts_count")
        Indication.create(user_id=user_id, kilowatts_count=kilowatts_count, created=datetime.now(), aggregator_id=aggregator_id)

        today = datetime.now().day
        indications = list(Indication.select().where((Indication.aggregator_id == aggregator_id) & (Indication.created.day == today)))
        total_kilowatts = sum([indication.kilowatts_count for indication in indications])
        last_lot = Lot.select().where(Lot.aggregator.id == int(aggregator_id)).order_by(Lot.id.desc()).first()
        if last_lot.total_kilowatts >= total_kilowatts * 0.98:
            electricities = list(Electricity.select().order_by(Electricity.amount_per_kilowatt.desc()))
            for electricity in electricities:
                electricity.total_kilowatts -= electricity.total_kilowatts_freeze
                electricity.total_kilowatts_freeze = 0
                electricity.save()

            last_lot.is_addition_order = True
            addition_kilowatts = last_lot.total_kilowatts * 0.10
            electricities = list(Electricity.select().order_by(Electricity.amount_per_kilowatt.desc()))
            total_free_kilowatts = sum(
                [(electricity.total_kilowatts - electricity.total_kilowatts_freeze) for electricity in electricities])

            preorder = {"kilowatt_count": 0, "amount": 0}

            if total_free_kilowatts > addition_kilowatts:
                for electricity in electricities:
                    if electricity.user != last_lot.aggregator:
                        free_kilowatts_count = electricity.total_kilowatts - electricity.total_kilowatts_freeze
                        if free_kilowatts_count > addition_kilowatts:
                            free_kilowatts_count = addition_kilowatts

                        addition_kilowatts -= free_kilowatts_count

                        preorder["kilowatt_count"] += free_kilowatts_count
                        preorder["amount"] += free_kilowatts_count * electricity.amount_per_kilowatt
                        electricity.total_kilowatts_freeze += free_kilowatts_count
                        electricity.save()

                average_price = preorder["amount"] / preorder["kilowatt_count"]

                last_lot.average_price = (last_lot.average_price * last_lot.total_kilowatts + average_price * preorder['kilowatt_count']) / (last_lot.total_kilowatts + preorder["kilowatt_count"])

                last_lot.kilowatts_number += preorder["kilowatt_count"]
                last_lot.save()

                last_lot.aggregator.wallet.balance -= preorder["amount"]
                last_lot.aggregator.wallet.save()

        return {"result": "OK"}

