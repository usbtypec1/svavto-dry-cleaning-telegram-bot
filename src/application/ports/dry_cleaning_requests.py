from typing import Protocol

from domain.entities.dry_cleaning_requests import (
    DryCleaningRequestReviewResult,
)


class DryCleaningRequestGateway(Protocol):

    async def approve(
            self,
            review_result: DryCleaningRequestReviewResult,
    ): ...

    async def reject(
            self,
            *,
            review_result: DryCleaningRequestReviewResult,
    ): ...
