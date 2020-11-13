from typing import NamedTuple, List

import db


class PaymentMethod(NamedTuple):
    codename: str
    name: str
    aliases: List[str]


class PaymentMethods:

    def __init__(self):
        self._payment_methods = self._load_payment_methods()

    @staticmethod
    def _load_payment_methods():
        payment_methods = db.fetch_all("payment_method", "codename name aliases".split())
        print(payment_methods)
        return payment_methods

    def get_all_payment_methods(self):
        return self._payment_methods
