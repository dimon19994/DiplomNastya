import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask
from flask_login import LoginManager

from config import BaseConfig
from constants import LotStatuses, AccountType, DEFAULT_COEFFICIENT

from models import open_db_connection, close_db_connection, User, Indication, Lot, Electricity
from utils import additional_order_kilowatts


def preorder_kilowatts():
    aggregators = list(User.select().where(User.account_type == AccountType.Aggregator))

    for aggregator in aggregators:
        yesterday = datetime.datetime.now().day - 1
        indications = list(Indication.select().where((Indication.aggregator_id == aggregator.id) & (Indication.created.day == yesterday)))
        total_kilowatts = sum([indication.kilowatts_count for indication in indications])
        last_lot = Lot.select().order_by(Lot.id.desc()).first()
        electricities = Electricity.select().order_by(Electricity.amount_per_kilowatt)

        if last_lot is not None:
            last_lot_kilowatts = last_lot.kilowatts_number
            for electricity in electricities:
                if last_lot_kilowatts < electricity.total_kilowatts_freeze:
                    last_lot_kilowatts = electricity.total_kilowatts_freeze
                last_lot_kilowatts -= electricity.total_kilowatts_freeze
                electricity.total_kilowatts -= electricity.total_kilowatts_freeze
                electricity.total_kilowatts_freeze = 0

                if last_lot_kilowatts == 0:
                    break

            if last_lot.kilowatts_number > total_kilowatts:
                kilowatts_for_sale = last_lot.kilowatts_number - total_kilowatts
                Electricity.create(total_kilowatts=kilowatts_for_sale, amount_per_kilowatt=last_lot.average_price*aggregator.addons.get("user_sale_coefficient", DEFAULT_COEFFICIENT), user=aggregator)

            if last_lot.is_addition_order:
                total_kilowatts *= 1.1

            last_lot.status = LotStatuses.Success
            last_lot.save()

        #заявка на покупку
        additional_order_kilowatts(total_kilowatts, aggregator)


def create_app(config=None):
    sched = BackgroundScheduler(daemon=True)
    # покупка
    sched.add_job(preorder_kilowatts, 'cron', hour=0, minute=22)
    sched.start()

    app = Flask(BaseConfig.PROJECT, instance_relative_config=True)

    login_manager = LoginManager()
    login_manager.login_view = 'main.login'
    login_manager.init_app(app)

    configure_app(app, config)

    configure_template_filters(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.get_or_none(User.id == int(user_id))

    return app


def configure_app(app, config=None):
    app.config.from_object(config or BaseConfig)

    from views import blueprint
    app.register_blueprint(blueprint)

    @app.before_request
    def _db_connect():
        open_db_connection()

    @app.teardown_request
    def _db_close(exc):
        close_db_connection()


def configure_template_filters(app):
    @app.template_filter()
    def lot_status(status):
        return LotStatuses.AllStatuses.get(str(status), "Undefined")
