import logging
from dataclasses import dataclass
from typing import Optional
from uuid import UUID

from src.application.dtos.artifact import ArtifactDTO, ArtifactAdmissionNotificationDTO, ArtifactCatalogPublicationDTO, \
    EraDTO, MaterialDTO
from src.application.interfaces.http_clients import ExternalMuseumAPIProtocol, PublicCatalogAPIProtocol
from src.application.interfaces.message_broker import MessageBrokerPublisherProtocol
from src.application.interfaces.repositories import ArtifactRepositoryProtocol
from src.application.mappers import ArtifactMapper
from src.domain.entities.artifact import ArtifactEntity

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class RegisterArtifactUseCase:
    repository: ArtifactRepositoryProtocol
    museum_api_client: ExternalMuseumAPIProtocol
    catalog_api_client: PublicCatalogAPIProtocol
    message_broker: MessageBrokerPublisherProtocol

    async def execute(self, inventory_id: UUID) -> ArtifactDTO:
        logger.info(f"Starting artifact registration for inventory_id={inventory_id}")

        artifact_entity: ArtifactEntity = await self.repository.get_by_inventory_id(str(inventory_id))
        if not artifact_entity:
            logger.info("Artifact not found locally, fetching from external service...")
            try:
                artifact_dto: ArtifactDTO = await self.museum_api_client.fetch_artifact(inventory_id)
                artifact_entity: ArtifactEntity = ArtifactMapper.to_entity(artifact_dto)
                await self.repository.save(artifact_entity)
            except Exception as e:
                logger.error(f"Failed to fetch artifact from external service: {e}")
                raise Exception("Could not fetch artifact from external service") from e

        artifact_notify_dto = ArtifactAdmissionNotificationDTO(
            inventory_id=artifact_entity.inventory_id,
            name=artifact_entity.name,
            acquisition_date=artifact_entity.acquisition_date,
            department=artifact_entity.department,
        )
        try:
            await self.message_broker.publish_new_artifact(artifact_notify_dto)
            logger.info("Published new artifact event to message broker")
        except Exception as e:
            logger.warning(f"Failed to publish message to broker: {e}")

        try:
            publication_dto = ArtifactCatalogPublicationDTO(
                inventory_id=artifact_entity.inventory_id,
                name=artifact_entity.name,
                era=EraDTO(value=artifact_entity.era.value),
                material=MaterialDTO(value=artifact_entity.material.value),
                description=artifact_entity.description,
            )
            public_id = await self.catalog_api_client.publish_artifact(publication_dto)
            logger.info(f"Artifact published to catalog with public_id={public_id}")
        except Exception as e:
            logger.error(f"Failed to publish artifact to catalog: {e}")
            raise Exception("Could not publish artifact to catalog") from e

        # Сохраняем обновленный артефакт (с public_id)

        logger.info(f"Artifact registration completed for inventory_id={inventory_id}")
        return artifact_dto
