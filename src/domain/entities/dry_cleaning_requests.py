import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.entities.enums.departments import Department
from domain.entities.enums.dry_cleaning_request_statuses import (
    DryCleaningRequestStatus,
)


class DryCleaningRequestService(BaseModel):
    id: UUID
    count: int


class DryCleaningRequest(BaseModel):
    id: int
    shift_id: int
    car_number: str
    photo_file_ids: list[str]
    services: list[DryCleaningRequestService]
    status: DryCleaningRequestStatus
    response_comment: str | None
    created_at: datetime.datetime
    updated_at: datetime.datetime


class DryCleaningRequestReviewResult(BaseModel):
    is_approved: bool
    dry_cleaning_request_id: int
    services: list[DryCleaningRequestService]
    comment: str | None
    department: Department
