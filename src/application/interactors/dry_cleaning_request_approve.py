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
        services = [
            {'id': service.id, 'count': service.count}
            for service in self.review_result.services
        ]
        await self.gateway.approve(
            request_id=self.review_result.dry_cleaning_request_id,
            services=services,
            comment=self.review_result.comment,
        )
