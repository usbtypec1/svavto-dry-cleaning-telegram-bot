from dataclasses import dataclass

from application.ports.dry_cleaning_requests import DryCleaningRequestGateway
from domain.entities.dry_cleaning_requests import (
    DryCleaningRequestReviewResult,
)


@dataclass(frozen=True, slots=True, kw_only=True)
class DryCleaningRequestApproveInteractor:
    review_result: DryCleaningRequestReviewResult
    gateway: DryCleaningRequestGateway

    async def execute(self):
        await self.gateway.approve(review_result=self.review_result)
