from collections.abc import Awaitable, Callable, Iterable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import Update


class WhitelistMiddleware(BaseMiddleware):

    def __init__(self, user_ids: Iterable[int]):
        self.__user_ids = set(user_ids)

    async def __call__(
            self,
            handler: Callable[[Update, dict[str, Any]],
            Awaitable[Any]],
            event: Update, data: dict[str, Any],
    ):
        user_id = None
        if event.message is not None:
            user_id = event.message.from_user.id
        elif event.callback_query is not None:
            user_id = event.callback_query.from_user.id
        if user_id in self.__user_ids:
            return await handler(event, data)
