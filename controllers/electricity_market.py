from flask import render_template
from flask_login import current_user

from constants import LotStatuses
from controllers import _Controller
from models import Lot


class ElectricityMarketController(_Controller):
    template = 'market.html'

    def _get(self):
        lots = list(Lot.select().where(Lot.status == LotStatuses.New, Lot.aggregator != current_user))
        return render_template(self.template, lots=lots)
