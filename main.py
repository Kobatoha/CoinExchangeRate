import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from crypto_price import get_crypto_price
from dotenv import load_dotenv
import asyncio
import os

load_dotenv()

TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

chat_data = {}


async def check_prices():
    while True:
        for chat_id, cryptos in chat_data.items():
            for crypto_symbol, thresholds in cryptos.items():
                current_price = get_crypto_price(crypto_symbol)
                min_threshold, max_threshold = thresholds

                if current_price < min_threshold:
                    await bot.send_message(
                        chat_id,
                        f'⚠️ {crypto_symbol} опустился ниже минимального порога! '
                        f'Текущая цена: {current_price:.2f} USD'
                    )
                elif current_price > max_threshold:
                    await bot.send_message(
                        chat_id,
                        f'🚀 {crypto_symbol} превысил максимальный порог! '
                        f'Текущая цена: {current_price:.2f} USD'
                    )

        await asyncio.sleep(60)  # Проверка каждые 60 секунд


@dp.message(Command("start"))
async def start(message: Message):
    chat_id = message.chat.id
    if chat_id not in chat_data:
        chat_data[chat_id] = {}
    await message.answer(
        "Привет! Отправь команду в формате /track BTC 30000 40000, чтобы следить за ценой криптовалюты."
    )


@dp.message(Command("track"))
async def track_crypto(message: types.Message):
    chat_id = message.chat.id

    try:
        _, crypto_symbol, min_threshold, max_threshold = message.text.split()
        min_threshold = float(min_threshold)
        max_threshold = float(max_threshold)

        if chat_id not in chat_data:
            chat_data[chat_id] = {}

        chat_data[chat_id][crypto_symbol.upper()] = (min_threshold, max_threshold)
        await message.answer(
            f"Теперь вы отслеживаете {crypto_symbol.upper()} с порогами {min_threshold} - {max_threshold} USD."
        )

    except ValueError:
        await message.answer(
            "Пожалуйста, введите данные в правильном формате: /track BTC 30000 40000"
        )


async def main():
    asyncio.create_task(check_prices())

    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
