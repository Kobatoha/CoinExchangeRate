import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import Message
from aiogram import F
from crypto_price import get_crypto_price
from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv('API_TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(Command("start"))
async def start(message: Message):
    await message.answer(
        "Привет! Отправь мне символ криптовалюты (например, BTC), и я расскажу тебе её текущую стоимость в USD.\n"
        "Можешь также указать пороговое значение, например: 'BTC 30000'."
    )


@dp.message(F.text.regexp(r'^\w+(\s+\d+(\.\d+)?)?$'))
async def send_crypto_price(message: Message):
    try:
        args = message.text.split()
        crypto_symbol = args[0].upper()
        threshold = float(args[1]) if len(args) > 1 else None

        price = get_crypto_price(crypto_symbol)

        if price:
            if threshold:
                if price >= threshold:
                    await message.answer(
                        f"⚠️ Внимание! Курс {crypto_symbol} достиг {price:.2f} USD, "
                        f"что выше или равно пороговому значению {threshold:.2f} USD."
                    )
                else:
                    await message.answer(
                        f"Курс {crypto_symbol} составляет {price:.2f} USD, "
                        f"что ниже порогового значения {threshold:.2f} USD."
                    )
            else:
                await message.answer(
                    f"Курс {crypto_symbol} составляет {price:.2f} USD."
                )
        else:
            await message.answer(
                "Не удалось получить данные о криптовалюте. Проверьте правильность символа."
            )
    except ValueError:
        await message.answer(
            "Пожалуйста, убедитесь, что вы указали корректное пороговое значение."
        )


async def main():
    logging.basicConfig(level=logging.INFO)

    dp.message.register(start, Command("start"))
    dp.message.register(send_crypto_price)

    await dp.start_polling(bot)

if __name__ == '__main__':
    import asyncio
    asyncio.run(main())
