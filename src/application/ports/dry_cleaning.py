from collections.abc import Iterable
from typing import Protocol
from uuid import UUID


class DryCleaningRequestGateway(Protocol):

    async def respond(
            self,
            *,
            request_id: int,
            approved_service_ids: Iterable[UUID],
            note: str | None,
    ): ...
