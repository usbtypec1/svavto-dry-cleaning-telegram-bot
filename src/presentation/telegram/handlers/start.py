from aiogram import Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.types import Message

from bootstrap.config import Config
from presentation.telegram.ui.views.base import answer_view
from presentation.telegram.ui.views.menu import MenuView


router = Router(name=__name__)


@router.message(
    CommandStart(),
    StateFilter('*'),
)
async def on_start(
        message: Message,
        config: Config,
) -> None:
    view = MenuView(
        msk_web_app_base_url=config.msk_web_app_base_url,
        spb_web_app_base_url=config.spb_web_app_base_url,
    )
    await answer_view(message, view)
