from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, WebAppInfo

from domain.entities.enums.departments import Department
from presentation.telegram.ui import button_texts
from presentation.telegram.ui.views.base import TextView


class DryCleaningRequestReviewView(TextView):
    text = '👇 Откройте меню для просмотра заявки на химчистку'

    def __init__(
            self,
            *,
            web_app_base_url: str,
            request_id: int,
            department: Department,
    ):
        self.__web_app_base_url = web_app_base_url
        self.__request_id = request_id
        self.__department = department

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        url = (
            f'{self.__web_app_base_url}'
            f'/dry-cleaning-requests/{self.__department}/{self.__request_id}/'
        )
        button = KeyboardButton(
            text=button_texts.DRY_CLEANING_REQUEST_REVIEW,
            web_app=WebAppInfo(url=url),
        )
        return ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[[button]])
