import datetime

from models import Indication, Lot, User

# for i in range(10):
#     yesterday = datetime.datetime.now() - datetime.timedelta(days=1, hours=i)
#     Indication.create(user_id=2, aggregator_id=1, kilowatts_count=10, created=yesterday)

for i in range(3):
    aggregator = User.select().first()
    Lot.create(status=0, aggregator=aggregator, average_price=50,
               kilowatts_number=1000)