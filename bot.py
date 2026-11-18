"""Мінімальний Telegram-бот СР ІПСА на aiogram 3.

Токен береться зі змінної середовища BOT_TOKEN:
  - локально — з файлу .env (див. .env.example);
  - на сервері — з apps/<назва>/shared/.env, задається командою `apps env <назва>`.

Файли, які мають переживати деплої (SQLite, JSON тощо), тримайте в папці data/.
"""
import asyncio
import logging
import os
import sys
from pathlib import Path

from aiogram import Bot, Dispatcher, F
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.types import Message

DATA_DIR = Path(__file__).parent / "data"

logging.basicConfig(
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("bot")

dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message) -> None:
    await message.answer(
        f"Привіт, {message.from_user.first_name}! 👋\n"
        "Це шаблонний бот СР ІПСА. /help — що я вмію."
    )


@dp.message(Command("help"))
async def help_(message: Message) -> None:
    await message.answer("/start — привітання\n/ping — перевірка, що бот живий")


@dp.message(Command("ping"))
async def ping(message: Message) -> None:
    await message.answer("pong 🏓")


@dp.message(F.text)
async def echo(message: Message) -> None:
    await message.answer("Не знаю такої команди. /help")


async def main() -> None:
    token = os.getenv("BOT_TOKEN")
    if not token:
        log.error("BOT_TOKEN не задано. На сервері: `apps env <назва бота>`, локально: файл .env")
        sys.exit(1)
    DATA_DIR.mkdir(exist_ok=True)
    bot = Bot(token, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    try:
        # Хибний токен або немає зв'язку з Telegram -> падаємо одразу,
        # щоб deploy-app побачив помилку і відкотив реліз
        me = await bot.get_me()
        log.info("Запущено як @%s", me.username)
        await dp.start_polling(bot)
    except Exception as e:  # noqa: BLE001 — будь-яка помилка старту = невдалий деплой
        log.error("Бот не запустився: %s: %s", type(e).__name__, e)
        sys.exit(1)
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        from dotenv import load_dotenv  # лише для локального запуску
        load_dotenv()
    except ImportError:
        pass
    asyncio.run(main())
