from flask import render_template, flash, redirect, url_for
from flask_login import current_user
from utils import additional_order_kilowatts

from controllers import _Controller
from models import User

class BuyElectricityController(_Controller):
    template = 'buy_electricity.html'

    def _post(self):
        total_kilowatts = int(self.request_data.get('total_kilowatts'))
        agregator = User.select().where(User.id == current_user).first()
        additional_order_kilowatts(total_kilowatts, agregator)

        return redirect(url_for("main.profile"))

    def _get(self):
        return render_template(self.template)
