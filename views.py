from flask import request, Blueprint, render_template
from flask_login import login_required
from flask_paginate import get_page_parameter, Pagination

from controllers.add_electricity import AddElectricityController
from controllers.add_lot import AddLotController
from controllers.buy_lot import BuyLotController
from controllers.delete_electricity import DeleteElectricityController
from controllers.delete_lot import DeleteLotController
from controllers.edit_coefficient import EditUserCoefficientController, \
    EditForeignUserCoefficientController,\
    EditUserLimitCoefficientController,\
    EditMinReserveCoefficientController
from controllers.edit_electricity import EditElectricityController
from controllers.edit_lot import EditLotController
from controllers.edit_wallet import EditWalletController
from controllers.electricity_market import ElectricityMarketController
from controllers.indication import IndicationController
from controllers.login import LoginController
from controllers.logout import LogoutController
from controllers.profile import ProfileController
from controllers.signup import SignUpController
from controllers.buy_electricity import BuyElectricityController
from models import Lot

blueprint = Blueprint('main', __name__)


@blueprint.route("/market", methods=["GET"])
@login_required
def electricity_market():
    return ElectricityMarketController(request).call()


@blueprint.route("/add_lot", methods=["GET", "POST"])
@login_required
def add_lot():
    return AddLotController(request).call()


@blueprint.route("/buy_lot/<lot_id>", methods=["GET", "POST"])
@login_required
def buy_lot(lot_id):
    return BuyLotController(request).call(lot_id)


@blueprint.route("/edit_lot/<lot_id>", methods=["GET", "POST"])
@login_required
def edit_lot(lot_id):
    return EditLotController(request).call(lot_id)


@blueprint.route("/delete_lot/<lot_id>", methods=["POST"])
@login_required
def delete_lot(lot_id):
    return DeleteLotController(request).call(lot_id)


@blueprint.route("/add_electricity", methods=["GET", "POST"])
@login_required
def add_electricity():
    return AddElectricityController(request).call()


@blueprint.route("/edit_electricity/<electricity_id>", methods=["GET", "POST"])
@login_required
def edit_electricity(electricity_id):
    return EditElectricityController(request).call(electricity_id)


@blueprint.route("/delete_electricity/<electricity_id>", methods=["POST"])
@login_required
def delete_electricity(electricity_id):
    return DeleteElectricityController(request).call(electricity_id)


@blueprint.route("/", methods=["GET"])
@blueprint.route("/profile", methods=["GET"])
@login_required
def profile():
    return ProfileController(request).call()


@blueprint.route("/logout", methods=["GET"])
def logout():
    return LogoutController(request).call()


@blueprint.route("/login", methods=['GET', 'POST'])
def login():
    return LoginController(request).call()


@blueprint.route("/signup", methods=['GET', 'POST'])
def signup():
    return SignUpController(request).call()


@blueprint.route("/indication/<aggregator_id>/<user_id>", methods=["POST"])
def indication(aggregator_id, user_id):
    return IndicationController(request).call(aggregator_id, user_id)


@blueprint.route("/edit_wallet", methods=["POST", "GET"])
def edit_wallet():
    return EditWalletController(request).call()


@blueprint.route("/edit_user_sale_coefficient", methods=["POST", "GET"])
def edit_user_sale_coefficient():
    return EditUserCoefficientController(request).call()


@blueprint.route("/edit_user_buy_coefficient", methods=["POST", "GET"])
def edit_user_buy_coefficient():
    return EditForeignUserCoefficientController(request).call()


@blueprint.route("/edit_user_limit_coefficient", methods=["POST", "GET"])
def edit_user_limit_coefficient():
    return EditUserLimitCoefficientController(request).call()


@blueprint.route("/edit_min_reserve_coefficient", methods=["POST", "GET"])
def edit_min_reserve_coefficient():
    return EditMinReserveCoefficientController(request).call()


@blueprint.route("/lots/<status>", methods=["POST", "GET"])
@blueprint.route("/lots", methods=["POST", "GET"])
def lots(status=None):
    page = int(request.args.get('page', 1))
    per_page = 10
    offset = (page - 1) * per_page

    lots = Lot.select()
    if status is not None:
        lots = lots.where(Lot.status == status)
    lots = lots.order_by(Lot.id.desc())
    lots_for_render = lots.limit(per_page).offset(offset)

    search = False

    q = request.args.get('q')
    if q:
        search = True

    pagination = Pagination(page=page, per_page=per_page, offset=offset,
                           total=lots.count(), css_framework='bulma',
                           search=search)

    return render_template('lots.html', lots=lots_for_render, pagination=pagination)


@blueprint.route("/buy_electricity", methods=["GET", "POST"])
@login_required
def buy_electricity():
    # todo покупка создать лот
    return BuyElectricityController(request).call()
