from flask import render_template, flash, redirect, url_for
from flask_login import current_user

from controllers import _Controller
from models import Electricity, User
from flask_paginate import Pagination


class ViewElectricityController(_Controller):
    template = 'view_electricitie.html'

    def _get(self):
        page = int(self.request.args.get('page', 1))
        per_page = 10
        offset = (page - 1) * per_page
        search = False

        electricitys = Electricity.select(User.name,
                                          (Electricity.total_kilowatts -
                                           Electricity.total_kilowatts_freeze).alias("kilowatts"),
                                          Electricity.amount_per_kilowatt.alias("amount")) \
            .join(User) \
            .where(Electricity.user != current_user)

        pagination_e = Pagination(page=page, per_page=per_page, offset=offset,
                                total=electricitys.count(), css_framework='bulma',
                                search=search)
        return render_template(self.template, electricitys=electricitys, pagination_e=pagination_e)
