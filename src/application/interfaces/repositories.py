from typing import Optional, Protocol
from uuid import UUID

from src.domain.entities.artifact import ArtifactEntity


class ArtifactRepositoryProtocol(Protocol):
    async def get_by_inventory_id(self, inventory_id: str | UUID) -> Optional[ArtifactEntity]:
        ...

    async def save(self, artifact: ArtifactEntity) -> None:
        ...
