from flask import render_template, flash, url_for, redirect
from werkzeug.security import generate_password_hash

from constants import AccountType, STATIONS
from controllers import _Controller
from eth import EthProtocol
from models import User

account_types = {"User": AccountType.User, "Salesman": AccountType.Salesman, "Aggregator": AccountType.Aggregator, "ForeignUser": AccountType.ForeignUser}


class SignUpController(_Controller):
    template = 'signup.html'

    def _post(self):
        email = self.request_data.get("email")
        name = self.request_data.get("name")
        password = self.request_data.get("password")
        account_type = account_types[self.request_data.get("account_type")]
        address = self.request_data.get("address")
        post_index = self.request_data.get("post_index")
        aggregator_id = self.request_data.get("aggregators")
        country = self.request_data.get("country")
        station = self.request_data.get("station")

        addons = dict(address=address, post_index=post_index, aggregator_id=aggregator_id, country=country,
                      station=station)

        user = User.get_or_none(User.email == email)

        if user is None:
            eth_protocol = EthProtocol()

            wallet = eth_protocol.create_wallet()

            User.create(
                email=email,
                name=name,
                password=generate_password_hash(password, method='sha256'),
                account_type=account_type,
                wallet=wallet,
                addons=addons
            )

            flash('Successful create account')
        else:
            flash('Email address already exists')
            return redirect(url_for("main.signup"))

        return redirect(url_for("main.login"))

    def _get(self):
        aggregators = list(User.select().where(User.account_type == AccountType.Aggregator))
        return render_template(self.template, aggregators=aggregators, stations=STATIONS)
