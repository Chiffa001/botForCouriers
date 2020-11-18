import logging

from config import API_TOKEN, ACCESS_ID
from payment_method import PaymentMethods
from delivery import add_delivery, get_today_deliveries, get_total_amount_per_day

from aiogram import Bot, Dispatcher, executor, types
from middlewares import AccessMiddleware

logging.basicConfig(level=logging.INFO)

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
dp.middleware.setup(AccessMiddleware(ACCESS_ID))


@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.message):
    await message.answer(
        "Бот для курьеров\n/help - помощь\n/payment - список алиасов\n"
        "/day - список всех доставок за день\n/total_amount_day - дневной итог")


@dp.message_handler(commands=['payment'])
async def process_payment_command(message: types.Message):
    payment_methods = PaymentMethods().get_all_payment_methods()
    answer_message = ""
    for string in [str(payment_method) for payment_method in payment_methods]:
        answer_message += f"{string}\n\n"
    await message.answer(answer_message)


@dp.message_handler(commands=['day'])
async def process_day_command(message: types.Message):
    today_deliveries = get_today_deliveries()
    if len(today_deliveries) == 0:
        await message.answer("Пока нет ни одной доставки")
        return
    today_deliveries = map(lambda delivery: f"Цена: {delivery[0]}\nСпособ оплаты: {delivery[1]}\n", today_deliveries)
    result = ""
    for key, string in enumerate(today_deliveries):
        result += f"Заказ {key + 1}:\n{string}\n"
    await message.answer(result)


@dp.message_handler(commands=['total_amount_day'])
async def process_total_amount_day_command(message: types.Message):
    total = get_total_amount_per_day()
    salary = len(get_today_deliveries()) * 3.9
    result = round(total - salary, 2)
    await message.answer(f"Всего: {str(total)}\nЗарплата: {salary}\nИтого: {result}\n")


@dp.message_handler()
async def process_any_command(message: types.Message):
    try:
        add_delivery(message.text)
        await message.answer("Добавлено")
    except:
        await message.answer("Что-то пошло не так")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
