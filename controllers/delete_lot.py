from flask import flash, redirect, url_for

from controllers import _Controller
from models import Lot, db


class DeleteLotController(_Controller):
    def _post(self, lot_id):
        lot = Lot.select().where(Lot.id == int(lot_id)).first()
        electricity = lot.electricity

        with db.atomic():
            electricity.total_kilowatts = electricity.total_kilowatts + lot.kilowatts_number
            electricity.total_kilowatts_freeze = electricity.total_kilowatts_freeze - lot.kilowatts_number
            electricity.save()

            lot.delete().execute()

        flash("Successful delete trading lot")

        return redirect(url_for("main.profile"))
