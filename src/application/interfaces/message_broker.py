from typing import Protocol

from src.application.dtos.artifact import ArtifactCatalogPublicationDTO


class MessageBrokerPublisherProtocol(Protocol):
    async def publish_new_artifact(self, artifact: ArtifactCatalogPublicationDTO) -> None:
        ...
