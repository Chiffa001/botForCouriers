from typing import NamedTuple, List, Dict

import db


class PaymentMethod(NamedTuple):
    codename: str
    name: str
    aliases: List[str]

    def __str__(self) -> str:
        return f"Способ оплаты: {self.name},\nВозможно указывать в виде: {self.aliases}"


class PaymentMethods:

    def __init__(self):
        self._payment_methods = self._load_payment_methods()

    @staticmethod
    def _load_payment_methods() -> List[PaymentMethod]:
        payment_methods = db.fetch_all("payment_method", "codename name aliases".split())
        payment_methods = PaymentMethods._fill_aliases(payment_methods)
        return payment_methods

    def get_all_payment_methods(self) -> List[PaymentMethod]:
        return self._payment_methods

    def get_payment_method_by_alias(self, alias) -> PaymentMethod:
        return list(filter(lambda m: alias in m.aliases or alias == m.name, self._payment_methods))[0]

    @staticmethod
    def _fill_aliases(payment_methods: List[Dict]) -> List[PaymentMethod]:
        payment_methods_result = []
        for payment_method in payment_methods:
            aliases = payment_method['aliases'].split(",")
            aliases = list(map(str.strip, aliases))

            payment_methods_result.append(PaymentMethod(
                codename=payment_method.get("codename"),
                name=payment_method.get("name"),
                aliases=aliases
            ))
        return payment_methods_result
