from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from controllers import _Controller
from eth import EthProtocol


class EditWalletController(_Controller):
    template = 'edit_wallet.html'

    def _post(self):
        amount = round(float(self.request_data.get("amount", 0)), 8)

        current_user.wallet.balance += amount
        current_user.wallet.save()

        flash("Баланс вдачно поповнено")

        return redirect(url_for("main.profile"))

    def _get(self):
        return render_template(self.template)
