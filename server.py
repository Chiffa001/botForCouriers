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
    PaymentMethods()
    await message.answer("Бот для курьеров")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
