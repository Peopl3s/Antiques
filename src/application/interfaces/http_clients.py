from typing import Protocol
from uuid import UUID

from src.application.dtos.artifact import ArtifactDTO, ArtifactCatalogPublicationDTO


class ExternalMuseumAPIProtocol(Protocol):
    async def fetch_artifact(self, inventory_id: str | UUID) -> ArtifactDTO:
        ...


class PublicCatalogAPIProtocol(Protocol):
    async def publish_artifact(self, artifact: ArtifactCatalogPublicationDTO) -> str:
        ...