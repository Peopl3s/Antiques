import json
import logging
from dataclasses import dataclass
from typing import final

from faststream.kafka import KafkaBroker

from src.application.dtos.artifact import ArtifactCatalogPublicationDTO
from src.application.interfaces.message_broker import MessageBrokerPublisherProtocol


@final
@dataclass(frozen=True, slots=True)
class KafkaPublisher(MessageBrokerPublisherProtocol):
    broker: KafkaBroker

    async def publish_new_artifact(self, artifact: ArtifactCatalogPublicationDTO) -> None:
        try:
            await self.broker.publish(
                message=json.dumps(artifact.model_dump(), ensure_ascii=False),
                topic="new_artifacts",
            )
        except Exception as e:
            logging.error(f"Failed to publish artifact: {e}")
            raise
