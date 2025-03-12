from dataclasses import dataclass

from application.ports.dry_cleaning_requests import DryCleaningRequestGateway
from domain.entities.dry_cleaning_requests import (
    DryCleaningRequestReviewResult,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DryCleaningRequestRejectInteractor:
    review_result: DryCleaningRequestReviewResult
    gateway: DryCleaningRequestGateway

    async def execute(self):
        await self.gateway.reject(
            request_id=self.review_result.dry_cleaning_request_id,
            comment=self.review_result.comment,
        )
