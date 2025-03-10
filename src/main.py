import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from bootstrap.config import load_config_from_file
from bootstrap.logger import setup_logging
from presentation.telegram.middlewares.whitelist import WhitelistMiddleware


async def main() -> None:
    config = load_config_from_file()
    setup_logging()
    bot = Bot(
        token=config.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    dispatcher.update.outer_middleware(
        WhitelistMiddleware(user_ids=config.whitelist_user_ids),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
