import logging

from config import API_TOKEN, ACCESS_ID
from payment_method import PaymentMethods

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

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
