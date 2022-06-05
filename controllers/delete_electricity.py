from flask import flash, redirect, url_for

from controllers import _Controller
from models import Electricity, Lot


class DeleteElectricityController(_Controller):
    def _post(self, electricity_id):
        electricity = Electricity.select().where(Electricity.id == int(electricity_id)).first()
        if not Lot.select().where(Lot.electricity == electricity).exists():
            electricity.delete().execute()
            flash("Successful delete  electricity")
        else:
            flash("Need delete lot with this electricity")

        return redirect(url_for("main.profile"))
