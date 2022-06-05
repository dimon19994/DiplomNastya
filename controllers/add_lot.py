from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from constants import LotStatuses
from controllers import _Controller
from models import Lot, Electricity, db


class AddLotController(_Controller):
    template = 'add_lot.html'

    def _post(self):
        amount_per_kilowatt = round(float(self.request_data.get('amount_per_kilowatt', 0)), 8)
        company_name = self.request_data.get('company_name')
        electricity_id = self.request_data.get('electricity_id')
        kilowatts_number = float(self.request_data.get('kilowatts_number', 0))

        electricity = Electricity.select().where(Electricity.id == int(electricity_id)).first()

        if electricity.total_kilowatts < kilowatts_number:
            flash("Number of kilowatts bigger total kilowatt count")
            return redirect(url_for("main.profile"))

        Lot.create(
            status=LotStatuses.New,
            amount_per_kilowatt=amount_per_kilowatt,
            salesman=current_user,
            company_name=company_name,
            electricity=electricity,
            kilowatts_number=kilowatts_number,
        )

        with db.atomic():
            electricity.total_kilowatts_freeze = kilowatts_number
            electricity.total_kilowatts = electricity.total_kilowatts - electricity.total_kilowatts_freeze
            electricity.save()

        flash("Successful create trading lot")

        return redirect(url_for("main.profile"))

    def _get(self):
        electricities = list(Electricity.select().where(Electricity.user == current_user))

        if len(electricities) == 0:
            flash("Need create electricity")
            return redirect(url_for("main.profile"))
        
        return render_template(self.template, electricities=electricities)
