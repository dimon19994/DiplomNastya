from functools import wraps

from flask_login import UserMixin
from peewee import (Model, CharField, datetime as peewee_datetime, IntegerField, ForeignKeyField, DoubleField, DateTimeField, BooleanField)
from playhouse.postgres_ext import PostgresqlExtDatabase, BinaryJSONField

from config import DB_CONFIG

peewee_now = peewee_datetime.datetime.now

db = PostgresqlExtDatabase(**DB_CONFIG)
db.commit_select = True
db.autorollback = True


def open_db_connection():
    if db.is_closed():
        db.connect()


def close_db_connection():
    if not db.is_closed():
        db.close()


def db_connect_wrapper(func):
    """
    connect to db and disconnect from it

    """

    @wraps(func)
    def wrapper(*args, **kwds):
        try:
            open_db_connection()
            return func(*args, **kwds)
        finally:
            close_db_connection()

    return wrapper


class _Model(Model):
    class Meta:
        database = db

    def __repr__(self):
        return "{class_name}(id={id})".format(class_name=self.__class__.__name__, id=self.id)

    @classmethod
    def get_by_id(cls, id):
        try:
            return cls.get(cls.id == id)
        except cls.DoesNotExist:
            return None


class Wallet(_Model):
    class Meta:
        db_table = "wallets"

    address = CharField(unique=True, index=True)
    password = CharField()
    balance = DoubleField()


class User(UserMixin, _Model):
    class Meta:
        db_table = "users"

    email = CharField(index=True, unique=True, max_length=255)
    password = CharField(max_length=255)
    name = CharField(max_length=255)
    account_type = IntegerField()
    wallet = ForeignKeyField(Wallet)
    addons = BinaryJSONField(default=dict())


class Indication(_Model):
    class Meta:
        db_table = "indications"

    user_id = IntegerField(index=True)
    aggregator_id = IntegerField(index=True)
    kilowatts_count = DoubleField()
    created = DateTimeField(default=peewee_now)


class Electricity(_Model):
    class Meta:
        db_table = "electricities"

    total_kilowatts = DoubleField()
    total_kilowatts_freeze = DoubleField(default=0)
    amount_per_kilowatt = DoubleField()
    user = ForeignKeyField(User)


class Lot(_Model):
    class Meta:
        db_table = "lots"

    status = IntegerField()
    aggregator = ForeignKeyField(User)
    average_price = DoubleField()
    kilowatts_number = DoubleField()
    is_addition_order = BooleanField(default=False)
    

if __name__ == '__main__':
    db.create_tables([Wallet, User, Electricity, Lot, Indication])
