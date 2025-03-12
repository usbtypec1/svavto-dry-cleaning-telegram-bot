import datetime
from uuid import UUID

from pydantic import BaseModel

from domain.entities.enums.departments import Department
from domain.entities.enums.dry_cleaning_request_statuses import (
    DryCleaningRequestStatus,
)


class DryCleaningRequestService(BaseModel):
    id: UUID
    name: str
    count: int
    is_countable: bool


class DryCleaningRequest(BaseModel):
    id: int
    shift_id: int
    car_number: str
    photo_urls: list[str]
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


class DryCleaningRequestOpen(BaseModel):
    dry_cleaning_request_id: int
