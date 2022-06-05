from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from controllers import _Controller
from models import Electricity


class AddElectricityController(_Controller):
    template = 'add_electricity.html'

    def _post(self):
        total_kilowatts = self.request_data.get('total_kilowatts')
        amount_per_kilowatt = self.request_data.get('amount_per_kilowatt')
        user = current_user

        Electricity.create(total_kilowatts=total_kilowatts, amount_per_kilowatt=amount_per_kilowatt, user=user)

        flash("Електроенергії додано вдачно")

        return redirect(url_for("main.profile"))

    def _get(self):
        return render_template(self.template)
