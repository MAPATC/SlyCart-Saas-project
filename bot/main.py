import logging
import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from config.config import Config, load_config
from handlers import main_menu


async def main():

    config: Config = load_config()

    bot = Bot(token=config.bot.token,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML))

    dp = Dispatcher()

    logging.basicConfig(
        level=config.log.log_level,
        format=config.log.log_format
    )

    dp.include_router(main_menu.router)

    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("Bot was stopped")


