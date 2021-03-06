from flask import render_template
from flask_login import current_user
from flask_paginate import Pagination

from constants import AccountType, DEFAULT_COEFFICIENT, DEFAULT_PRIORITY, MIN_RESERVE, USER_LIMIT, sale_priority, buy_priority
from controllers import _Controller
from eth import EthProtocol
from models import Lot, Electricity, User


class ProfileController(_Controller):
    template = 'profile_{}.html'

    def _get(self):
        if current_user.account_type in [AccountType.User, AccountType.ForeignUser, AccountType.Salesman]:
            page = int(self.request.args.get('page', 1))
            per_page = 10
            offset = (page - 1) * per_page
            search = False

            electricitys = Electricity.select(User.name,
                                              (Electricity.total_kilowatts -
                                               Electricity.total_kilowatts_freeze).alias("kilowatts"),
                                              Electricity.amount_per_kilowatt.alias("amount")) \
                .join(User) \
                .where(Electricity.user == current_user)

            pagination_e = Pagination(page=page, per_page=per_page, offset=offset,
                                      total=electricitys.count(), css_framework='bulma',
                                      search=search)

            lots = Lot.select().where(Lot.aggregator == current_user).order_by(Lot.id.desc())
            lots_for_render = lots.limit(per_page).offset(offset)

            q = self.request.args.get('q')
            if q:
                search = True

            pagination = Pagination(page=page, per_page=per_page, offset=offset,
                                    total=lots.count(), css_framework='bulma',
                                    search=search)

            user_limit = current_user.addons.get("user_limit", USER_LIMIT)
            min_reserve = current_user.addons.get("min_reserve", MIN_RESERVE)
            country = current_user.addons.get("country")

            if current_user.account_type == AccountType.User:
                return render_template(self.template.format("user"), lots=lots_for_render, pagination=pagination,
                                       user_limit=user_limit, min_reserve=min_reserve)
            elif current_user.account_type == AccountType.ForeignUser:
                return render_template(self.template.format("foreign"), lots=lots_for_render, pagination=pagination,
                                       country=country, electricitys=electricitys, pagination_e=pagination_e)
            elif current_user.account_type == AccountType.Salesman:
                return render_template(self.template.format("salesman"), lots=lots_for_render, pagination=pagination,
                                       user_limit=user_limit)

        elif current_user.account_type == AccountType.Aggregator:
            user_sale_coefficient = current_user.addons.get("user_sale_coefficient", DEFAULT_COEFFICIENT)
            user_buy_coefficient = current_user.addons.get("user_buy_coefficient", DEFAULT_COEFFICIENT)
            user_sale_foreign_coefficient = current_user.addons.get("user_sale_foreign_coefficient", DEFAULT_COEFFICIENT)
            user_buy_foreign_coefficient = current_user.addons.get("user_buy_foreign_coefficient", DEFAULT_COEFFICIENT)
            user_buy_priority = buy_priority.get(current_user.addons.get("user_buy_priority", [1, 2, 3])[0])
            user_sale_priority = sale_priority.get(current_user.addons.get("user_sale_priority", [1, 2, 3])[0])
            return render_template(
                self.template.format("aggregator"),
                user_sale_coefficient=user_sale_coefficient,
                user_buy_coefficient=user_buy_coefficient,
                user_sale_foreign_coefficient=user_sale_foreign_coefficient,
                user_buy_foreign_coefficient=user_buy_foreign_coefficient,
                user_buy_priority=user_buy_priority,
                user_sale_priority=user_sale_priority,
            )
