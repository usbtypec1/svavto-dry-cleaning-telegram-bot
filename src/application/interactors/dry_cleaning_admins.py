from dataclasses import dataclass

from application.ports.dry_cleaning_admins import DryCleaningAdminGateway


@dataclass(frozen=True, slots=True, kw_only=True)
class DryCleaningAdminsListInteractor:
    gateway: DryCleaningAdminGateway

    async def execute(self) -> list[int]:
        return await self.gateway.get_all()
