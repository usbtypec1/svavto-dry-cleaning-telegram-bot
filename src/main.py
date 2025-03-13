import asyncio

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.types import BotCommand

from bootstrap.config import load_config_from_file
from bootstrap.logger import setup_logging
import presentation.telegram.handlers
from presentation.telegram.middlewares.whitelist import WhitelistMiddleware


def include_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.include_routers(
        presentation.telegram.handlers.dry_cleaning_requests.router,
        presentation.telegram.handlers.start.router,
    )


async def setup_commands(bot: Bot) -> None:
    await bot.set_my_commands(
        [
            BotCommand(
                command='start',
                description='Меню бота',
            ),
        ]
    )


async def main() -> None:
    config = load_config_from_file()
    setup_logging()
    bot = Bot(
        token=config.telegram_bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    await setup_commands(bot)
    dispatcher = Dispatcher()
    dispatcher['config'] = config
    include_handlers(dispatcher)
    dispatcher.update.outer_middleware(
        WhitelistMiddleware(user_ids=config.whitelist_user_ids),
    )
    await bot.delete_webhook(drop_pending_updates=True)
    await dispatcher.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
