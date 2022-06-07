class AccountType:
    User = 0
    Salesman = 1
    Aggregator = 2
    ForeignUser = 3


class LotStatuses:
    New = 0
    Success = 1

    AllStatuses = {
        "0": "Открыта",
        "1": "Закрыта",
    }


DEFAULT_COEFFICIENT = 0.95
USER_LIMIT = 100000
MIN_RESERVE = 50000


DEFAULT_PRIORITY = {
    "buy": {
        1: AccountType.User,
        2: AccountType.ForeignUser,
        3: AccountType.Salesman
    },
    "sale": {
        1: AccountType.Salesman,
        2: AccountType.User,
        3: AccountType.ForeignUser
    }
}

STATIONS = {
    "AES": "Атомна електоренергія",
    "GES": "Гідро електоренергія",
    "TES": "Тепло електоренергія",
    "AltES": "Альтернативна електоренергія",
}

sale_priority = {
    1: "Зберігач електроенергії",
    2: "Користувач електроенергії",
    3: "Іноземний користувач",
}

buy_priority = {
    1: "Користувач електроенергії",
    2: "Іноземний користувач",
    3: "Зберігач електроенергії",
}
