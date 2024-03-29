from typing import NamedTuple, List, Dict
import re
import db
import pytz
from datetime import datetime
from payment_method import PaymentMethods


def add_delivery(raw_message: str):
    message = _parse_message(raw_message.lower())
    if _check_number(message):
        payment_method, amount = "cash", float(message)
    else:
        payment_method, amount = PaymentMethods().get_payment_method_by_alias(
            message).codename, 0

    db.insert("delivery", {
        "amount": amount,
        "created": _get_now_formatted(),
        "payment_codename": payment_method,
        "rate_id": 1,
        "raw_text": raw_message
    })

    # PaymentMethods().get_payment_method_by_alias(message)


def get_today_deliveries() -> []:
    cursor = db.get_cursor()
    cursor.execute(
        "select amount, (select name from payment_method where codename = delivery.payment_codename) "
        "from delivery where date(created) = date('now', 'localtime')")
    result = cursor.fetchall()
    return result


def get_total_amount_per_day() -> float:
    cursor = db.get_cursor()
    cursor.execute("select sum(amount) from delivery where date(created) = date('now', 'localtime')")
    return cursor.fetchone()[0] or 0


def _parse_message(raw_message: str):
    regexp_result = re.match(r"^([\d]+.?([\d]+)?)|([а-я]+)", raw_message)
    return regexp_result.group(0)


def _check_number(string: str) -> bool:
    return string.replace('.', '', 1).isdigit()


def _get_now_datetime() -> datetime:
    tz = pytz.timezone("Europe/Moscow")
    return datetime.now(tz)


def _get_now_formatted():
    return _get_now_datetime().strftime("%Y-%m-%d %H:%M:%S")
