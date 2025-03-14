import datetime
from collections.abc import Awaitable, Callable
from typing import Any

import httpx
from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, Update

from application.interactors.dry_cleaning_admins import (
    DryCleaningAdminsListInteractor,
)
from bootstrap.config import Config
from infrastructure.adapters.application.dry_cleaning_admins import (
    DryCleaningAdminGateway,
)


class AdminUserIdsMiddleware(BaseMiddleware):

    def __init__(self, config: Config):
        self.__updated_at: datetime.datetime | None = None
        self.__admin_user_ids: set[int] | None = None
        self.__config = config

    async def __update_admin_user_ids(self) -> None:
        admin_ids: set[int] = set()
        for base_url in (
                self.__config.api.msk_base_url,
                self.__config.api.spb_base_url,
        ):

            async with httpx.AsyncClient(base_url=base_url) as http_client:
                gateway = DryCleaningAdminGateway(http_client)
                admin_ids.update(
                    await DryCleaningAdminsListInteractor(
                        gateway=gateway,
                    ).execute()
                )
        self.__admin_user_ids = admin_ids
        self.__updated_at = datetime.datetime.now(datetime.UTC)

    def __is_expired(self) -> bool:
        if self.__updated_at is None:
            return True
        expires_at = self.__updated_at + datetime.timedelta(seconds=60)
        return datetime.datetime.now(datetime.UTC) > expires_at

    async def __get_admin_user_ids(self) -> set[int]:
        if self.__admin_user_ids is None or self.__is_expired():
            await self.__update_admin_user_ids()
        return self.__admin_user_ids

    async def __call__(
            self,
            handler: Callable[
                [TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: Update,
            data: dict[str, Any],
    ):
        admin_user_ids = await self.__get_admin_user_ids()
        data['admin_user_ids'] = admin_user_ids

        if event.message is not None:
            user_id = event.message.from_user.id
        elif event.callback_query is not None:
            user_id = event.callback_query.from_user.id
        else:
            return

        if user_id in admin_user_ids:
            return await handler(event, data)
