from dataclasses import dataclass
import logging
from typing import TYPE_CHECKING, cast
from uuid import UUID

from src.application.dtos.artifact import (
    ArtifactAdmissionNotificationDTO,
    ArtifactCatalogPublicationDTO,
    ArtifactDTO,
    EraDTO,
    MaterialDTO,
)
from src.application.exceptions import (
    ArtifactNotFoundError,
    FailedFetchArtifactMuseumAPIException,
    FailedPublishArtifactInCatalogException,
    FailedPublishArtifactMessageBrokerException,
)
from src.application.interfaces.http_clients import (
    ExternalMuseumAPIProtocol,
    PublicCatalogAPIProtocol,
)
from src.application.interfaces.mappers import DtoEntityMapperProtocol
from src.application.interfaces.message_broker import MessageBrokerPublisherProtocol
from src.application.interfaces.repositories import ArtifactRepositoryProtocol

if TYPE_CHECKING:
    from src.domain.entities.artifact import ArtifactEntity

logger = logging.getLogger(__name__)


@dataclass(frozen=True, slots=True, kw_only=True)
class GetArtifactUseCase:
    repository: ArtifactRepositoryProtocol
    museum_api_client: ExternalMuseumAPIProtocol
    catalog_api_client: PublicCatalogAPIProtocol
    message_broker: MessageBrokerPublisherProtocol
    artifact_mapper: DtoEntityMapperProtocol

    async def execute(self, inventory_id: str | UUID) -> ArtifactDTO:
        inventory_id_str = (
            str(inventory_id) if isinstance(inventory_id, UUID) else inventory_id
        )
        logger.info(
            "Starting artifact registration", extra={"inventory_id": inventory_id_str}
        )

        artifact_dto: ArtifactDTO | None = None
        artifact_entity: (
            ArtifactEntity | None
        ) = await self.repository.get_by_inventory_id(str(inventory_id))
        if not artifact_entity:
            logger.info("Artifact not found locally, fetching from external service...")
            try:
                artifact_dto = await self.museum_api_client.fetch_artifact(inventory_id)
                artifact_entity = self.artifact_mapper.to_entity(artifact_dto)
                await self.repository.save(artifact_entity)
            except ArtifactNotFoundError as e:
                logger.exception(
                    "Artifact not found in external museum API",
                    extra={"inventory_id": inventory_id, "error": str(e)},
                )
            except Exception as e:
                logger.exception(
                    "Failed to fetch artifact from external museum API",
                    extra={"inventory_id": inventory_id, "error": str(e)},
                )
                raise FailedFetchArtifactMuseumAPIException(
                    "Could not fetch artifact from external service",
                    str(e),
                ) from e

        artifact_notify_dto = ArtifactAdmissionNotificationDTO(
            inventory_id=artifact_entity.inventory_id,
            name=artifact_entity.name,
            acquisition_date=artifact_entity.acquisition_date,
            department=artifact_entity.department,
        )
        try:
            await self.message_broker.publish_new_artifact(artifact_notify_dto)
            logger.info(
                "Published new artifact event to message broker",
                extra={"inventory_id": inventory_id_str},
            )
        except Exception as e:
            logger.warning(
                "Failed to publish message to broker (non-critical)",
                extra={"inventory_id": artifact_entity.inventory_id, "error": str(e)},
            )
            raise FailedPublishArtifactMessageBrokerException(
                "Failed to publish message to broker",
                str(e),
            ) from e

        publication_dto = ArtifactCatalogPublicationDTO(
            inventory_id=artifact_entity.inventory_id,
            name=artifact_entity.name,
            era=EraDTO(
                value=cast(
                    "Literal['paleolithic', 'neolithic', 'bronze_age', 'iron_age', 'antiquity', 'middle_ages', 'modern']",
                    artifact_entity.era.value,
                ),
            ),
            material=MaterialDTO(
                value=cast(
                    "Literal['ceramic', 'metal', 'stone', 'glass', 'bone', 'wood', 'textile', 'other']",
                    artifact_entity.material.value,
                ),
            ),
            description=artifact_entity.description,
        )
        try:
            public_id: str = await self.catalog_api_client.publish_artifact(
                publication_dto
            )
            logger.info(
                "Artifact published to catalog",
                extra={
                    "inventory_id": artifact_entity.inventory_id,
                    "public_id": public_id,
                },
            )
        except Exception as e:
            logger.exception(
                "Failed to publish artifact to catalog",
                extra={"inventory_id": artifact_entity.inventory_id, "error": str(e)},
            )
            raise FailedPublishArtifactInCatalogException(
                "Could not publish artifact to catalog", str(e)
            ) from e

        logger.info(
            "Artifact registration completed",
            extra={"inventory_id": inventory_id_str},
        )
        return artifact_dto or self.artifact_mapper.to_dto(artifact_entity)
