from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from constants import LotStatuses
from controllers import _Controller
from eth import EthProtocol
from models import Lot, Electricity, db


class BuyLotController(_Controller):
    template = "buy_lot.html"

    def _post(self, lot_id):
        eth_protocol = EthProtocol()

        kilowatts_number = float(self.request_data.get('kilowatts_number', 0))
        lot = Lot.select().where(Lot.id == int(lot_id)).first()
        electricity = lot.electricity

        if kilowatts_number > lot.kilowatts_number:
            flash("Input number so biggest")
            return redirect(url_for('main.electricity_market'))

        wallet_balance = eth_protocol.get_balance(current_user.wallet)

        lot_amount = round(lot.amount_per_kilowatt * kilowatts_number, 8)

        if wallet_balance < lot_amount:
            flash("Amount bigger wallet balance")
            return redirect(url_for('main.electricity_market'))

        with db.atomic():
            lot.kilowatts_number -= kilowatts_number
            if lot.kilowatts_number == 0:
                lot.status = LotStatuses.Success

            electricity.total_kilowatts_freeze -= kilowatts_number
            electricity.save()

            tx_hash = eth_protocol.send_eth_transaction(current_user.wallet, current_user.wallet.password, lot.aggregator.wallet.address, lot_amount)
            lot.transactions_history[tx_hash] = kilowatts_number
            lot.save()

            Electricity.create(user=current_user, electricity_type=lot.electricity.electricity_type, total_kilowatts=kilowatts_number)

        flash("Successful buy lot")

        return redirect(url_for("main.profile"))

    def _get(self, lot_id):
        lot = Lot.select().where(Lot.id == int(lot_id)).first()
        return render_template(self.template, lot=lot)