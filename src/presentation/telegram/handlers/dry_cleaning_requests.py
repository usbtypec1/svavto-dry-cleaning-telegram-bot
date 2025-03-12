from typing import assert_never

import httpx
from aiogram import F, Router
from aiogram.filters import StateFilter
from aiogram.types import CallbackQuery, Message

from application.interactors.dry_cleaning_request_approve import \
    DryCleaningRequestApproveInteractor
from application.interactors.dry_cleaning_request_reject import \
    DryCleaningRequestRejectInteractor
from bootstrap.config import Config
from domain.entities.dry_cleaning_requests import \
    (
    DryCleaningRequestOpen, DryCleaningRequestReviewResult,
)
from domain.entities.enums.departments import Department
from infrastructure.adapters.application.dry_cleaning_requests import \
    DryCleaningRequestGateway
from presentation.telegram.callback_data.dry_cleaning_requests import (
    DryCleaningRequestReviewCallbackData,

)
from presentation.telegram.ui import button_texts
from presentation.telegram.ui.views.base import answer_view
from presentation.telegram.ui.views.dry_cleaning_requests import (
    DryCleaningRequestReviewView, DryCleaningRequestView,
)
from presentation.telegram.ui.views.menu import MenuView


router = Router(name=__name__)


@router.message(
    F.web_app_data.button_text == button_texts.DRY_CLEANING_REQUEST_REVIEW,
    StateFilter('*'),
)
async def on_dry_cleaning_request_response(
        message: Message,
        config: Config,
) -> None:
    review_result = DryCleaningRequestReviewResult.model_validate_json(
        message.web_app_data.data,
    )
    if review_result.department == Department.MSK:
        base_url = config.api.msk_base_url
    elif review_result.department == Department.SPB:
        base_url = config.api.spb_base_url
    else:
        assert_never(review_result.department)

    async with httpx.AsyncClient(base_url=base_url) as http_client:
        gateway = DryCleaningRequestGateway(http_client)
        if review_result.is_approved:
            await DryCleaningRequestApproveInteractor(
                gateway=gateway,
                review_result=review_result,
            ).execute()
        else:
            await DryCleaningRequestRejectInteractor(
                gateway=gateway,
                review_result=review_result,
            ).execute()

    await message.answer('✅ Запрос на химчистку успешно обработан')
    view = MenuView(
        msk_web_app_base_url=config.web_app.msk_base_url,
        spb_web_app_base_url=config.web_app.spb_base_url,
    )
    await answer_view(message, view)


@router.callback_query(
    DryCleaningRequestReviewCallbackData.filter(),
    StateFilter('*'),
)
async def on_show_dry_cleaning_request_review_menu(
        callback_query: CallbackQuery,
        callback_data: DryCleaningRequestReviewCallbackData,
        config: Config,
) -> None:
    if callback_data.department == Department.MSK:
        base_url = config.web_app.msk_base_url
    elif callback_data.department == Department.SPB:
        base_url = config.web_app.spb_base_url
    else:
        assert_never(callback_data.department)

    view = DryCleaningRequestReviewView(
        web_app_base_url=base_url,
        department=callback_data.department,
        request_id=callback_data.dry_cleaning_request_id,
    )
    await answer_view(callback_query.message, view)


@router.message(
    F.web_app_data.button_text == button_texts.DRY_CLEANING_REQUEST_LIST_MSK,
    StateFilter('*'),
)
async def on_show_dry_cleaning_request_list_msk(
        message: Message,
        config: Config,
) -> None:
    dry_cleaning_request = DryCleaningRequestOpen.model_validate_json(
        message.web_app_data.data,
    )
    async with httpx.AsyncClient(
            base_url=config.api.msk_base_url,
    ) as http_client:
        gateway = DryCleaningRequestGateway(http_client)
        dry_cleaning_request = await gateway.get_by_id(
            dry_cleaning_request.dry_cleaning_request_id,
        )

    view = DryCleaningRequestView(dry_cleaning_request)
    await answer_view(message, view)

    view = DryCleaningRequestReviewView(
        web_app_base_url=config.web_app.msk_base_url,
        department=Department.MSK,
        request_id=dry_cleaning_request.id,
    )
    await answer_view(message, view)


@router.message(
    F.web_app_data.button_text == button_texts.DRY_CLEANING_REQUEST_LIST_SPB,
    StateFilter('*'),
)
async def on_show_dry_cleaning_request_list_spb(
        message: Message,
        config: Config,
) -> None:
    dry_cleaning_request = DryCleaningRequestOpen.model_validate_json(
        message.web_app_data.data,
    )
    async with httpx.AsyncClient(
            base_url=config.api.spb_base_url,
    ) as http_client:
        gateway = DryCleaningRequestGateway(http_client)
        dry_cleaning_request = await gateway.get_by_id(
            dry_cleaning_request.dry_cleaning_request_id,
        )

    view = DryCleaningRequestView(dry_cleaning_request)
    await answer_view(message, view)

    view = DryCleaningRequestReviewView(
        web_app_base_url=config.web_app.spb_base_url,
        department=Department.SPB,
        request_id=dry_cleaning_request.id,
    )
    await answer_view(message, view)
