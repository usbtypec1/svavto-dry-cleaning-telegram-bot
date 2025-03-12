from aiogram.filters.callback_data import CallbackData

from domain.entities.enums.departments import Department


class DryCleaningRequestReviewCallbackData(
    CallbackData,
    prefix='dry_cleaning_request',
):
    dry_cleaning_request_id: int
    department: Department
