from aiogram.types import (
    InputMediaPhoto, KeyboardButton, ReplyKeyboardMarkup,
    WebAppInfo,
)

from domain.entities.dry_cleaning_requests import DryCleaningRequest
from domain.entities.enums.departments import Department
from presentation.telegram.ui import button_texts
from presentation.telegram.ui.views.base import MediaGroupView, TextView


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


class DryCleaningRequestView(MediaGroupView):

    def __init__(self, dry_cleaning_request: DryCleaningRequest):
        self.__dry_cleaning_request = dry_cleaning_request

    def get_medias(self) -> list[InputMediaPhoto]:
        return [
            InputMediaPhoto(media=photo_url)
            for photo_url in self.__dry_cleaning_request.photo_urls
        ]

    def get_caption(self) -> str:
        lines: list[str] = [
            f'<b>Сотрудник {self.__dry_cleaning_request.staff_full_name}'
            ' запрашивает химчистку:</b>'
        ]
        for service in self.__dry_cleaning_request.services:
            if service.is_countable:
                lines.append(f'{service.name} - {service.count} шт.')
            else:
                lines.append(service.name)
        return '\n'.join(lines)
