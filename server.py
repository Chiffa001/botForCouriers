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
    await message.answer("Бот для курьеров")


@dp.message_handler(commands=['payment'])
async def get_payment_methods(message: types.Message):
    payment_methods = PaymentMethods().get_all_payment_methods()
    answer_message = ""
    for string in [str(payment_method) for payment_method in payment_methods]:
        answer_message += f"{string}\n\n"
    await message.answer(answer_message)


@dp.message_handler(commands=['day'])
async def get_list_of_today_deliveries(message: types.Message):
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
async def send_sum_per_day(message: types.Message):
    total = get_total_amount_per_day()
    await message.answer(f"Всего: {str(total)}")


@dp.message_handler()
async def echo(message: types.Message):
    try:
        add_delivery(message.text)
        await message.answer("end")
    except Exception:
        await message.answer("Что-то пошло не так")


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
