from flask import render_template, flash, redirect, url_for

from controllers import _Controller
from models import Electricity


class EditElectricityController(_Controller):
    template = 'edit_electricity.html'

    def _post(self, electricity_id):
        electricity = Electricity.select().where(Electricity.id == int(electricity_id)).first()

        electricity.electricity_type = self.request_data.get("electricity_type")
        electricity.total_kilowatts = self.request_data.get("total_kilowatts")
        electricity.save()

        flash("Successful edit electricity")

        return redirect(url_for("main.profile"))

    def _get(self, electricity_id):
        electricity = Electricity.select().where(Electricity.id == int(electricity_id)).first()
        return render_template(self.template, electricity=electricity)
