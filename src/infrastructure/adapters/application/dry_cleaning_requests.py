from dataclasses import dataclass

import httpx

from domain.entities.dry_cleaning_requests import (
    DryCleaningRequest, DryCleaningRequestReviewResult,
)


@dataclass(frozen=True, slots=True)
class DryCleaningRequestGateway:
    http_client: httpx.AsyncClient

    async def get_by_id(
            self,
            dry_cleaning_request_id: int,
    ) -> DryCleaningRequest:
        url = f'/dry-cleaning/requests/{dry_cleaning_request_id}/'
        response = await self.http_client.get(url)
        return DryCleaningRequest.model_validate_json(response.text)

    async def approve(
            self,
            review_result: DryCleaningRequestReviewResult,
    ):
        url = (
            '/dry-cleaning/requests'
            f'/{review_result.dry_cleaning_request_id}/approve/'
        )
        request_data = {
            'response_comment': review_result.comment,
            'services': [
                {'id': str(service.id), 'count': service.count}
                for service in review_result.services
            ]
        }
        response = await self.http_client.post(url, json=request_data)

    async def reject(
            self,
            review_result: DryCleaningRequestReviewResult,
    ):
        url = (
            '/dry-cleaning/requests'
            f'/{review_result.dry_cleaning_request_id}/reject/'
        )
        request_data = {'response_comment': review_result.comment}
        response = await self.http_client.post(url, json=request_data)
