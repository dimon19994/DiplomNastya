from flask import render_template, flash, redirect, url_for

from controllers import _Controller
from models import Lot


class EditLotController(_Controller):
    template = 'edit_lot.html'

    def _post(self, lot_id):
        lot = Lot.select().where(Lot.id == int(lot_id)).first()

        lot.amount_per_kilowatt = self.request_data.get("amount_per_kilowatt")
        lot.company_name = self.request_data.get("company_name")
        lot.save()

        flash("Successful edit lot")

        return redirect(url_for("main.profile"))

    def _get(self, lot_id):
        lot = Lot.select().where(Lot.id == int(lot_id)).first()
        return render_template(self.template, lot=lot)
