from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from presentation.telegram.ui.views.base import TextView


class MenuView(TextView):
    text = 'Главное меню'

    def __init__(
            self,
            *,
            msk_web_app_base_url: str,
            spb_web_app_base_url: str,
    ):
        self.__msk_web_app_base_url = msk_web_app_base_url
        self.__spb_web_app_base_url = spb_web_app_base_url

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        return ReplyKeyboardMarkup(
            resize_keyboard=True,
            is_persistent=True,
            keyboard=[
                [
                    KeyboardButton(
                        text='[МСК] Заявки на химчистку',
                        web_app=WebAppInfo(
                            url=f'{self.__msk_web_app_base_url}'
                                f'/dry-cleaning-requests',
                        ),
                    ),
                    KeyboardButton(
                        text='[СПБ] Заявки на химчистку',
                        web_app=WebAppInfo(
                            url=f'{self.__spb_web_app_base_url}'
                                f'/dry-cleaning-requests',
                        ),
                    ),
                ]
            ]
        )
