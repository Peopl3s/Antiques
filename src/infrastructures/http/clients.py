import logging
from dataclasses import dataclass
from typing import final
from uuid import UUID

import httpx
import stamina

from src.application.dtos.artifact import ArtifactDTO, ArtifactCatalogPublicationDTO
from src.application.exceptions import ArtifactNotFoundError
from src.application.interfaces.http_clients import ExternalMuseumAPIProtocol, PublicCatalogAPIProtocol

logger = logging.getLogger(__name__)


@final
@dataclass(frozen=True, slots=True)
class ExternalMuseumAPIClient(ExternalMuseumAPIProtocol):
    base_url: str
    client: httpx.AsyncClient

    @stamina.retry(
        on=(httpx.HTTPError, httpx.RequestError),
        attempts=3,
        wait_initial=0.5,
        wait_jitter=1.0,
    )
    async def fetch_artifact(self, inventory_id: str | UUID) -> ArtifactDTO:
        inventory_id_str = str(inventory_id)
        url = f"{self.base_url}/artifacts/{inventory_id_str}"
        logger.debug(f"Fetching artifact from URL: {url}")

        try:
            response = await self.client.get(url)
            if response.status_code == 404:
                logger.warning(f"Artifact {inventory_id_str} not found (404).")
                raise ArtifactNotFoundError(f"Artifact {inventory_id_str} not found in external service")

            response.raise_for_status()
            data = response.json()

            artifact = ArtifactDTO(
                inventory_id=data["inventory_id"],
                name=data["name"],
                era=data["era"],
                material=data["material"],
                description=data["description"],
                acquisition_date=data["acquisition_date"],
                department=data["department"],
            )
            logger.debug(f"Successfully fetched artifact: {artifact}")
            return artifact

        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.error(f"HTTP error while fetching artifact {inventory_id_str}: {e}")
            raise
        except ValueError as e:
            logger.error(f"Data validation error for artifact {inventory_id_str}: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error while fetching artifact {inventory_id_str}: {e}")
            raise


@final
@dataclass(frozen=True, slots=True)
class PublicCatalogAPIClient(PublicCatalogAPIProtocol):
    base_url: str
    client: httpx.AsyncClient

    @stamina.retry(
        on=(httpx.HTTPError, httpx.RequestError),
        attempts=3,
        wait_initial=1.0,
        wait_jitter=1.0,
    )
    async def publish_artifact(self, artifact: ArtifactCatalogPublicationDTO) -> str:
        """
        Publishes an artifact to the public catalog and returns its public ID.

        Raises:
            httpx.HTTPStatusError: If the response status is not successful.
            httpx.RequestError: If there is a network problem.
            ValueError: If the response JSON does not contain 'public_id'.
            Exception: For any other unexpected errors.
        """
        url = f"{self.base_url}/items"
        payload = {
            "inventory_id": artifact.inventory_id,
            "name": artifact.name,
            "era": artifact.era,
            "material": artifact.material,
            "description": artifact.description,
        }
        logger.debug("Publishing artifact to URL %s with payload: %s", url, payload)

        try:
            response = await self.client.post(url, json=payload, timeout=httpx.Timeout(10.0))
            response.raise_for_status()
            data = response.json()
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            logger.error("Error during HTTP request to %s: %s", url, e)
            raise
        except Exception as e:
            logger.error("Unexpected error during publishing artifact: %s", e)
            raise Exception(f"Failed to publish artifact to catalog: {e}") from e

        public_id = data.get("public_id")
        if not public_id:
            logger.error("Response JSON missing 'public_id' field: %s", data)
            raise ValueError("Invalid response data: missing 'public_id'")

        logger.debug("Successfully published artifact, public_id: %s", public_id)
        return public_id

