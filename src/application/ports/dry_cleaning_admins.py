from typing import Protocol


class DryCleaningAdminGateway(Protocol):

    async def get_all(self) -> list[int]: ...
