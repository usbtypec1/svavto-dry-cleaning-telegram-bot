from dataclasses import dataclass

import httpx


@dataclass(frozen=True, slots=True)
class DryCleaningAdminGateway:
    http_client: httpx.AsyncClient

    async def get_all(self) -> list[int]:
        url = '/dry-cleaning/admins/'
        response = await self.http_client.get(url)
        return [admin['id'] for admin in response.json()['admins']]
